import requests
from typing import Dict, Any
import time
from bs4 import BeautifulSoup
import trafilatura


class TextExtractor:
    """
    Text extraction tool for the Global Information Trend Assessment system.
    Extracts relevant text data from URLs using trafilatura and fallback methods.
    """

    def __init__(self, timeout: int = 10, max_content_chars: int = 100000):
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
    def extract_text(self, url: str) -> str:
        """
        Extract relevant text content from a given URL.
        Uses trafilatura for high-quality extraction with fallback to BeautifulSoup.
        """
        if not url or not url.startswith("http"):
            return "[SKIPPED invalid URL]"

        try:
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()
        except Exception as e:
            return f"[ERROR fetching page: {e}]"

        html = resp.text

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
        try:
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
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