import requests
from datetime import datetime
import time


class GDELTClient:
    """
    Realistic wrapper for GDELT DOC 2.0 API.

    Core API: https://api.gdeltproject.org/api/v2/doc/doc
    Supports:
    - Article search (artlist)
    - Timeline volume (timelinevol)
    - Image/galleries (optional modes)
    """

    BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    # -----------------------------
    # Core request handler
    # -----------------------------
    def _get(self, params: dict):
        # Add delay between requests as required by GDELT API
        time.sleep(7)
        response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    # -----------------------------
    # Article search (ARTLIST)
    # -----------------------------
    def search_articles(
        self,
        query: str,
        timespan: str = None,
        startdatetime: str = None,
        enddatetime: str = None,
        maxrecords: int = 75,
        sort: str = "HybridRel",
        format: str = "json",
    ):
        """
        Article search using artlist mode.

        IMPORTANT (from GDELT docs):
        - You can use EITHER TIMESPAN OR START/ENDDATETIME, not both.
        - Default coverage is last ~3 months unless constrained.
        """

        params = {
            "query": query,
            "mode": "artlist",
            "format": format,
            "sort": sort,
            "maxrecords": maxrecords,
        }

        # Time window mode (offset-based)
        if timespan:
            params["timespan"] = timespan

        # Precise datetime window
        if startdatetime:
            params["startdatetime"] = startdatetime
        if enddatetime:
            params["enddatetime"] = enddatetime

        return self._get(params)

    # -----------------------------
    # Timeline (trend analysis)
    # -----------------------------
    def timeline(self, query: str, timespan: str = "1d", smooth: int = 5):
        """
        Volume timeline of coverage.

        Uses mode=timelinevol
        """

        params = {
            "query": query,
            "mode": "timelinevol",
            "timespan": timespan,
            "TIMELINESMOOTH": smooth,
            "format": "json",
        }

        return self._get(params)

    # -----------------------------
    # Image / visual narrative mode
    # -----------------------------
    def image_gallery(
        self,
        query: str,
        timespan: str = "1w",
        mode: str = "imagegallery",
        maxrecords: int = 50,
    ):
        """
        Visual news narrative (image-based zeitgeist signals)
        """

        params = {
            "query": query,
            "mode": mode,
            "timespan": timespan,
            "format": "json",
            "maxrecords": maxrecords,
        }

        return self._get(params)

    # -----------------------------
    # Convenience: Zeitgeist pull
    # -----------------------------
    def zeitgeist_snapshot(self, topics: list):
        """
        Compare multiple narratives in one snapshot.
        """

        results = {}

        for topic in topics:
            results[topic] = {
                "articles": self.search_articles(topic),
                "trend": self.timeline(topic, timespan="1d"),
            }

        return results

    # -----------------------------
    # Helper: datetime formatter
    # -----------------------------
    @staticmethod
    def dt_to_gdelt(dt: datetime) -> str:
        """
        Convert datetime -> GDELT format YYYYMMDDHHMMSS
        """
        return dt.strftime("%Y%m%d%H%M%S")
