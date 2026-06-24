#!/usr/bin/env python3
"""
Test script for the SearchDatabase implementation.
Demonstrates how it works with serper_search and text_extractor.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.search_database import SearchDatabase
from tools.serper_search import SerperSearch
from tools.text_extractor import TextExtractor

def test_database():
    """Test the database functionality."""

    print("Testing Search Database")
    print("=" * 30)

    # Initialize database
    db = SearchDatabase()

    # Test database statistics
    stats = db.get_statistics()
    print(f"Initial Statistics: {stats}")

    # Test storing a result manually (simulating what would come from serper_search + text_extractor)
    test_result = {
        "url": "https://example.com/article1",
        "title": "Example Article About AI",
        "content": "Artificial intelligence is transforming many industries. Machine learning algorithms are being used to solve complex problems in healthcare, finance, and transportation.",
        "search_query": "artificial intelligence applications",
        "date_posted": "2026-06-23"
    }

    success = db.store_result(
        url=test_result["url"],
        title=test_result["title"],
        content=test_result["content"],
        search_query=test_result["search_query"]
    )

    print(f"Stored test result: {success}")

    # Test retrieving the result
    retrieved = db.get_result_by_url("https://example.com/article1")
    if retrieved:
        print(f"Retrieved result title: {retrieved['title']}")

    # Test search functionality
    print("\nTesting search functionality:")
    search_results = db.search("artificial intelligence", limit=5)
    print(f"Found {len(search_results)} results for 'artificial intelligence'")

    if search_results:
        for result in search_results[:2]:  # Show first 2 results
            print(f"  - {result['title']} ({result['url']})")

    # Test recent results
    print("\nRecent results:")
    recent = db.get_recent_results(3)
    for result in recent:
        print(f"  - {result['title']} (added {result['timestamp']})")

    # Test statistics after adding data
    stats = db.get_statistics()
    print(f"\nStatistics after adding data: {stats}")

if __name__ == "__main__":
    test_database()