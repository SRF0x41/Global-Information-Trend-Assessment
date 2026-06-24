import requests
from typing import Dict, List, Any
import time
import os
from dotenv import load_dotenv


class SerperSearch:
    """
    Serper search tool for the Global Information Trend Assessment system.
    Uses the Serper API for web searches.
    """

    def __init__(self, timeout: int = 10):
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = "https://google.serper.dev/search"

        # Load environment variables if not provided directly
        if self.api_key is None:
            load_dotenv()
            self.api_key = os.getenv("SERPER_API_KEY")

        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json",
            }
        )

    def search(self, query: str) -> List[Dict[str, str]]:
        payload = {"q": query}

        try:
            resp = self.session.post(self.base_url, json=payload, timeout=self.timeout)
            resp.raise_for_status()

            # Add 5-second delay after search
            time.sleep(5)

        except Exception as e:
            raise RuntimeError(f"Search request failed: {e}")

        data = resp.json()

        results = []

        # Handle organic search results - only extract from the "organic" list
        if "organic" in data:
            for result in data["organic"]:
                results.append(
                    {
                        "title": result.get("title", ""),
                        "url": result.get("link", ""),
                        "snippet": result.get("snippet", ""),
                        "date": result.get("date", ""),
                    }
                )

        return results
