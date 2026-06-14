import requests
import json


class DataFetcher:
    def fetch(self, url):
        """
        Fetch data from a given URL.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None
