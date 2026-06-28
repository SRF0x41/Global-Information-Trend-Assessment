import logging
import io
import requests
from typing import Dict, Any, Optional
import time
from bs4 import BeautifulSoup
import trafilatura
from pypdf import PdfReader

logger = logging.getLogger(__name__)


class TextExtractor:
    """
    Text extraction tool for the Information Trend Assessment system.
    Extracts relevant text data from URLs using trafilatura and fallback methods.
    """

    def __init__(self, timeout: int = 10, max_content_chars: int = 60000):
        self.session = requests.Session()
        self.timeout = timeout
        self.max_content_chars = max_content_chars

        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                )
            }
        )

    # ----------------------------
    # EXTRACT TEXT FROM URL
    # ----------------------------
    def _fetch_url(self, url: str) -> Optional[str]:
        """
        Fetch a URL and return the HTML body.
        Returns None on 4xx/5xx responses or network errors.
        """
        if not url or not url.startswith("http"):
            return None

        try:
            resp = self.session.get(url, timeout=self.timeout)
            if resp.status_code >= 400:
                logger.warning("Skipping URL %s — HTTP %s", url, resp.status_code)
                return None
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            logger.warning("Error fetching %s: %s", url, e)
            return None

    def _fetch_bytes(self, url: str) -> Optional[bytes]:
        """Fetch a URL and return raw bytes. Returns None on error."""
        if not url or not url.startswith("http"):
            return None

        try:
            resp = self.session.get(url, timeout=self.timeout)
            if resp.status_code >= 400:
                logger.warning("Skipping URL %s — HTTP %s", url, resp.status_code)
                return None
            resp.raise_for_status()
            return resp.content
        except Exception as e:
            logger.warning("Error fetching %s: %s", url, e)
            return None

    def _extract_pdf(self, data: bytes) -> str:
        """Extract text from PDF data."""
        try:
            reader = PdfReader(io.BytesIO(data))
            texts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    texts.append(page_text)
            result = "\n\n".join(texts)
            return result[:self.max_content_chars]
        except Exception as e:
            logger.warning("PDF extraction failed: %s", e)
            return "[ERROR could not parse PDF]"

    _VERIFICATION_INDICATORS = [
        'please verify you are a human',
        'are you a robot',
        'complete the challenge',
        'verifying you are not a robot',
        'cloudflare-turnstile',
        'cf-challenge',
        'under attack mode',
        'checking your device',
        'captcha',
        'recaptcha',
        'h-captcha',
        'age verification',
        'verify your age',
        'you must be 13 or older',
        'reddit.com/r/verify',
        'one-time code',
        'enter the code',
        'security check',
        'prove you are human',
    ]

    def _is_verification_page(self, html: str) -> bool:
        """Heuristic: detect verification gates / interstitials."""
        soup = BeautifulSoup(html, "html.parser")
        # Lowercase title + body text for matching
        title = (soup.title.get_text() if soup.title else "").lower()
        body = soup.get_text(separator=" ", lowercase=True)
        # Scan a trimmed window — full page text is overkill
        check = (title + " " + body[:5000])
        return any(indicator in check for indicator in self._VERIFICATION_INDICATORS)

    def extract_text(self, url: str) -> str:
        """
        Extract relevant text content from a given URL.
        Supports HTML (trafilatura + BeautifulSoup fallback) and PDF files.
        Returns "[SKIPPED ...]" on invalid URLs, HTTP errors, or skipped domains.
        """
        # Skip Reddit entirely — verification gates produce no useful content
        if "reddit.com" in url.lower():
            return "[SKIPPED reddit — verification gate]"

        data = self._fetch_bytes(url)
        if data is None:
            return "[SKIPPED could not fetch page]"

        # Detect PDF by file signature (%PDF header bytes)
        if data.startswith(b"%PDF"):
            return self._extract_pdf(data)

        html = data.decode("utf-8", errors="ignore")

        # Skip verification gates / interstitials (Cloudflare, Reddit verify, CAPTCHA, etc.)
        if self._is_verification_page(html):
            return "[SKIPPED verification gate detected]"

        # Try high-quality extractor first (trafilatura)
        try:
            extracted = trafilatura.extract(html)
            if extracted:
                return extracted[: self.max_content_chars]
        except Exception:
            pass

        # Fallback: BeautifulSoup extraction
        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted elements
        for tag in soup(
            ["script", "style", "noscript", "header", "footer", "nav", "aside"]
        ):
            tag.decompose()

        # Extract text content
        text = soup.get_text(separator="\n")

        # Clean up text
        lines = [line.strip() for line in text.splitlines()]
        clean_text = "\n".join(line for line in lines if line)

        return clean_text[: self.max_content_chars]

    # ----------------------------
    # EXTRACT WITH METADATA
    # ----------------------------
    def extract_with_metadata(self, url: str) -> Dict[str, Any]:
        """
        Extract text content along with metadata from a URL.
        """
        start = time.time()

        content = self.extract_text(url)
        elapsed = time.time() - start

        # Try to extract title if possible
        title = ""
        html = self._fetch_url(url)
        if html:
            try:
                soup = BeautifulSoup(html, "html.parser")
                title_tag = soup.find("title")
                if title_tag:
                    title = title_tag.get_text().strip()
            except Exception:
                pass

        return {
            "url": url,
            "title": title,
            "content": content,
            "elapsed_seconds": round(elapsed, 3),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    # ----------------------------
    # BATCH EXTRACT
    # ----------------------------
    def batch_extract(self, urls: list) -> list:
        """
        Extract text content from multiple URLs.
        """
        results = []

        for url in urls:
            # Add 5-second delay between requests to prevent rate limiting
            time.sleep(5)

            result = self.extract_with_metadata(url)
            results.append(result)

        return results
