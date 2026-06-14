from analysis.document_collector import DocumentCollector
import time

def main():
    collector = DocumentCollector()

    print(f"Starting RSS feed scraping at {time.ctime()}")

    for item in collector.scrape_all_rss_feeds():
        # Basic example - just print the title and URL
        print(f"\nTitle: {item['content'].split('\n')[0]}")
        print(f"URL: {item['metadata']['url']}")
        print("-" * 80)

    print(f"\nFinished RSS feed scraping at {time.ctime()}")

if __name__ == "__main__":
    main()