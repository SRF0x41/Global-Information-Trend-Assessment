import yaml
import requests
import feedparser
import time
from pathlib import Path


class DocumentCollector:

    def _load_feeds(self):
        config_path = Path(__file__).parent.parent / "sources" / "feeds.yaml"

        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def scrape_all_rss_feeds(self):
        feeds = self._load_feeds()

        for category, feed_list in feeds.items():
            for feed in feed_list:
                yield from self.scrape_rss_feed(feed["url"])

    def scrape_rss_feed(self, url):
        try:
            response = requests.get(
                url, timeout=10, headers={"User-Agent": "DocumentCollector/1.0"}
            )

            response.raise_for_status()

            feed = feedparser.parse(response.content)

            if feed.bozo:
                print(f"Warning parsing {url}: " f"{feed.bozo_exception}")

            if not feed.entries:
                print(f"No entries found in {url}")
                return

            for entry in feed.entries:

                title = getattr(entry, "title", "")
                description = getattr(entry, "description", "")

                yield {
                    "source": url,
                    "content": f"{title}\n\n{description}",
                    "metadata": {
                        "url": getattr(entry, "link", ""),
                        "score": getattr(entry, "score", 0),
                        "created_utc": getattr(
                            entry,
                            "published_parsed",
                            time.gmtime(),
                        ),
                    },
                }

        except Exception as e:
            print(f"Error scraping RSS feed " f"{url}: {e}")
