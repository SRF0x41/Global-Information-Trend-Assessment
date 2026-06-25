import requests
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class LmStudioClient:
    """
    A client for interacting with LM Studio and other OpenAI-compatible APIs.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:1234/v1",
        api_key: str = "not-needed",
        timeout=None,
        response_log_dir: str = "llm_responses",
    ):
        """
        Initialize the client.

        Args:
            base_url: The base URL of the API (e.g., "http://127.0.0.1:1234/v1").
            api_key: The API key (not typically needed for local servers).
            timeout: Timeout in seconds for request operations.
            response_log_dir: Directory to write streamed responses to disk.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.response_log_dir = response_log_dir
        self.logger = logging.getLogger(__name__)

    # ------------------------------------------------------------------
    # REPEAT DETECTION
    # ------------------------------------------------------------------
    @staticmethod
    def _detect_repeat(text: str, window_size: int = 300, min_repeat: int = 10) -> bool:
        """
        Check if the end of *text* is stuck in a repeat loop.

        Looks at the last ``window_size`` characters and tests whether any
        substring of length ``min_repeat`` .. window_size//2 appears
        consecutively 3+ times to fill the window.
        """
        if len(text) < window_size:
            return False
        window = text[-window_size:]
        for length in range(min_repeat, window_size // 2 + 1):
            candidate = window[:length]
            repeats = window_size // length
            if repeats >= 3 and candidate * repeats == window[:repeats * length]:
                return True
        return False

    # ------------------------------------------------------------------
    # DISK LOGGING
    # ------------------------------------------------------------------
    def _get_log_path(self, purpose: str = "response") -> Path:
        """Return a fresh log directory for this batch of attempts."""
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_dir = Path(self.response_log_dir) / f"{ts}_{purpose}"
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

    def _write_log(self, log_dir: Path, attempt: int, content: str, status: str):
        """Append current content to the per-attempt log file."""
        log_file = log_dir / f"response_{attempt}.md"
        header = f"# Attempt {attempt} — [{status}]\n\n---\n\n"
        # Write header only on first write for this attempt
        if not log_file.exists():
            log_file.write_text(header, encoding="utf-8")
        log_file.open("a", encoding="utf-8").write(content)

    # ------------------------------------------------------------------
    # STREAMING WITH REPEAT DETECTION
    # ------------------------------------------------------------------
    def send_streaming(
        self,
        user: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 5,
        purpose: str = "response",
    ) -> Optional[str]:
        """
        Stream a chat completion, detect repeat loops, log to disk, retry on loop.

        Returns the best (longest) non-looped response, or the best partial
        response if all attempts looped.
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})

        log_dir = self._get_log_path(purpose)
        best_response: Optional[str] = None

        for attempt in range(1, max_retries + 2):  # 1 original + max_retries
            try:
                response = self._stream_completion(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    log_dir=log_dir,
                    attempt=attempt,
                )
                # Successful (non-looped) response
                if response is not None and not response.startswith("[LOOPED] "):
                    content = response
                    if best_response is None or len(content) > len(best_response):
                        best_response = content
                    # If we got a good response, no need to retry
                    break
                else:
                    # Loop detected — save partial and retry
                    partial = response.replace("[LOOPED] ", "") if response else None
                    if partial and (best_response is None or len(partial) > len(best_response)):
                        best_response = partial

            except Exception as e:
                self.logger.error(f"Streaming attempt {attempt} failed: {e}")
                continue

        return best_response

    def _stream_completion(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        log_dir: Optional[Path] = None,
        attempt: int = 1,
    ) -> Optional[str]:
        """
        Perform a single streaming chat completion.

        Returns the accumulated content string. If a repeat loop is detected,
        aborts early and returns content prefixed with ``[LOOPED] ``.
        """
        url = f"{self.base_url}/chat/completions"
        payload = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        session = requests.Session()
        accumulated = []

        try:
            resp = session.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout,
                stream=True,
            )
            resp.raise_for_status()

            for line in resp.iter_lines():
                if not line:
                    continue
                line_str = line.decode("utf-8") if isinstance(line, bytes) else line
                if not line_str.startswith("data: "):
                    continue
                data = line_str[6:]
                if data == "[DONE]":
                    break
                try:
                    import json
                    chunk = json.loads(data)
                    delta = (
                        chunk.get("choices", [{}])[0]
                        .get("delta", {})
                        .get("content", "")
                    )
                    if delta:
                        accumulated.append(delta)
                        # Write to disk immediately
                        if log_dir:
                            self._write_log(log_dir, attempt, delta, "STREAMING")

                        # Check for repeats periodically (every 10 deltas)
                        if len(accumulated) % 10 == 0:
                            full = "".join(accumulated)
                            if self._detect_repeat(full):
                                # Strip the repeated tail
                                content = self._strip_repeat_tail(full)
                                self._write_log(
                                    log_dir, attempt, "\n\n[LOOP DETECTED]", "LOOPED"
                                )
                                return "[LOOPED] " + content
                except json.JSONDecodeError:
                    continue

            content = "".join(accumulated)
            if log_dir:
                self._write_log(log_dir, attempt, "\n\n[COMPLETE]", "OK")
            return content

        except requests.RequestException as e:
            self.logger.error(f"Streaming error: {e}")
            content = "".join(accumulated)
            if log_dir and content:
                self._write_log(log_dir, attempt, "\n\n[ERROR: " + str(e) + "]", "ERROR")
            return content if content else None
        finally:
            session.close()

    @staticmethod
    def _strip_repeat_tail(text: str, window_size: int = 300) -> str:
        """Remove the repeating tail from text, keeping only the clean portion."""
        if len(text) <= window_size:
            return text
        return text[:-window_size]

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def list_models(self) -> Dict[str, Any]:
        """List available models."""
        url = f"{self.base_url}/models"
        try:
            response = requests.get(
                url, headers=self._get_headers(), timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error listing models: {e}")
            raise

    def send(
        self,
        user: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Optional[str]:
        """
        Convenience wrapper for chat completions using system + user prompts.
        Returns assistant content or None on failure.
        """

        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": user})

        try:
            response = self.chat_completions(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Safe extraction (prevents KeyError crashes)
            return response.get("choices", [{}])[0].get("message", {}).get("content")

        except Exception as e:
            self.logger.error(f"Chat completion failed in send(): {e}")
            return None

    def chat_completions(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a chat completion.
        """
        url = f"{self.base_url}/chat/completions"
        payload = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": stop,
            "stream": stream,
        }
        # Remove None values to avoid sending them in the payload
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            response = requests.post(
                url, headers=self._get_headers(), json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error in chat completions: {e}")
            raise

    def completions(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a completion.
        """
        url = f"{self.base_url}/completions"
        payload = {
            "prompt": prompt,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": stop,
            "stream": stream,
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            response = requests.post(
                url, headers=self._get_headers(), json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error in completions: {e}")
            raise

    def embeddings(
        self,
        input: Union[str, List[str]],
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get embeddings for the given input.
        """
        url = f"{self.base_url}/embeddings"
        payload = {
            "input": input,
            "model": model,
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            response = requests.post(
                url, headers=self._get_headers(), json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error in embeddings: {e}")
            raise

    def responses(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a response (custom endpoint provided by user).
        """
        url = f"{self.base_url}/responses"
        payload = {"messages": messages, "model": model, **kwargs}
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            response = requests.post(
                url, headers=self._get_headers(), json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error in responses: {e}")
            raise

    def __repr__(self) -> str:
        return f"<LmStudioAPI(base_url='{self.base_url}')>"
