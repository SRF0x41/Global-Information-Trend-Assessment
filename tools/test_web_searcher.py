#!/usr/bin/env python3
"""
Test script for WebSearcher class
"""

from web_searcher import WebSearcher

def main():
    # Create an instance of WebSearcher
    searcher = WebSearcher()

    # Perform a simple search
    print("Performing a simple search...")
    results = searcher.search("Python programming", 5)

    for result in results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Snippet: {result['snippet']}")
        print("-" * 50)

    # Perform a detailed search
    print("\nPerforming a detailed search...")
    detailed_results = searcher.search_detailed("machine learning", 3)

    print(f"Query: {detailed_results['query']}")
    print(f"Total results: {detailed_results['total_results']}")
    print(f"Timestamp: {detailed_results['timestamp']}")

    for result in detailed_results['results']:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Snippet: {result['snippet']}")
        print("-" * 50)

if __name__ == "__main__":
    main()