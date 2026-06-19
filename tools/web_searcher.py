import requests
from typing import Dict, List, Any
from bs4 import BeautifulSoup
import time
import urllib.parse


class WebSearcher:
    """
    Lightweight web searcher + full page reader
    using DuckDuckGo HTML results.
    """

    def __init__(self, timeout: int = 10, max_content_chars: int = 8000):
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
    # CLEAN DUCKDUCKGO URLS
    # ----------------------------
    def clean_url(self, url: str) -> str:
        """
        Converts DuckDuckGo redirect URLs into real URLs.
        """
        if not url:
            return ""

        if url.startswith("//"):
            url = "https:" + url

        if "uddg=" in url:
            parsed = urllib.parse.urlparse(url)
            qs = urllib.parse.parse_qs(parsed.query)

            if "uddg" in qs:
                return urllib.parse.unquote(qs["uddg"][0])

        return url

    # ----------------------------
    # SEARCH
    # ----------------------------
    def search(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        url = "https://duckduckgo.com/html/"
        params = {"q": query}

        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Search request failed: {e}")

        soup = BeautifulSoup(resp.text, "html.parser")

        results = []
        links = soup.find_all("a", class_="result__a")

        for link in links[:num_results]:
            title = link.get_text()
            raw_url = link.get("href")
            url = self.clean_url(raw_url)

            snippet = ""
            parent = link.find_parent("div", class_="result")

            if parent:
                snippet_tag = parent.find("a", class_="result__snippet")
                if snippet_tag:
                    snippet = snippet_tag.get_text()

            results.append(
                {
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                }
            )

        return results

    # ----------------------------
    # FETCH PAGE CONTENT
    # ----------------------------
    def fetch_page(self, url: str) -> str:
        if not url or not url.startswith("http"):
            return "[SKIPPED invalid URL]"

        try:
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()
        except Exception as e:
            return f"[ERROR fetching page: {e}]"

        html = resp.text

        # Try high-quality extractor first
        try:
            import trafilatura

            extracted = trafilatura.extract(html)
            if extracted:
                return extracted[:self.max_content_chars]
        except Exception:
            pass

        # Fallback: BeautifulSoup extraction
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(
            ["script", "style", "noscript", "header", "footer", "nav", "aside"]
        ):
            tag.decompose()

        text = soup.get_text(separator="\n")

        lines = [line.strip() for line in text.splitlines()]
        clean_text = "\n".join(line for line in lines if line)

        return clean_text[:self.max_content_chars]

    # ----------------------------
    # SEARCH + READ
    # ----------------------------
    def search_and_read(self, query: str, num_results: int = 3) -> List[Dict[str, Any]]:
        results = self.search(query, num_results=num_results)

        enriched = []

        for r in results:
            content = self.fetch_page(r["url"])

            enriched.append(
                {
                    "title": r["title"],
                    "url": r["url"],
                    "snippet": r["snippet"],
                    "content": content,
                }
            )

        return enriched

    # ----------------------------
    # META WRAPPER
    # ----------------------------
    def search_detailed(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        start = time.time()
        results = self.search(query, num_results)
        elapsed = time.time() - start

        return {
            "query": query,
            "total_results": len(results),
            "results": results,
            "elapsed_seconds": round(elapsed, 3),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }