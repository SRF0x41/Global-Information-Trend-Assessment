import requests
import logging
from typing import Any, Dict, List, Optional, Union

class LmStudioClient:
    """
    A client for interacting with LM Studio and other OpenAI-compatible APIs.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:1234/v1",
        api_key: str = "not-needed",
        timeout = None,
    ):
        """
        Initialize the client.

        Args:
            base_url: The base URL of the API (e.g., "http://127.0.0.1:1234/v1").
            api_key: The API key (not typically needed for local servers).
            timeout: Timeout in seconds for request operations.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def list_models(self) -> Dict[str, Any]:
        """List available models."""
        url = f"{self.base_url}/models"
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error listing models: {e}")
            raise

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
            response = requests.post(url, headers=self._get_headers(), json=payload, timeout=self.timeout)
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
            response = requests.post(url, headers=self._get_headers(), json=payload, timeout=self.timeout)
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
            response = requests.post(url, headers=self._get_headers(), json=payload, timeout=self.timeout)
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
        payload = {
            "messages": messages,
            "model": model,
            **kwargs
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            response = requests.post(url, headers=self._get_headers(), json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error in responses: {e}")
            raise

    def __repr__(self) -> str:
        return f"<LmStudioAPI(base_url='{self.base_url}')>"

