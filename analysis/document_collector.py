import yaml
from praw.models import Submission
from bs4 import BeautifulSoup
import requests

class DocumentCollector:
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        with open("../sources/reddit.yaml") as f:
            return yaml.safe_load(f)

    def collect_reddit_posts(self):
        import praw

        reddit = praw.Reddit(
            client_id=self.config["client_id"],
            client_secret=self.config["client_secret"],
            user_agent=self.config["user_agent"]
        )

        for subreddit in self.config["subreddits"]:
            for submission in reddit.subreddit(subreddit).new(limit=self.config["max_posts"]):
                if not submission.is_self:
                    yield {
                        "source": f"r/{subreddit}",
                        "content": submission.title + "\n\n" + submission.selftext,
                        "metadata": {
                            "url": submission.url,
                            "score": submission.score,
                            "created_utc": submission.created_utc
                        }
                    }