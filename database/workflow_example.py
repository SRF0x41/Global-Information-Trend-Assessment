#!/usr/bin/env python3
"""
Complete workflow example showing how serper_search, text_extractor, and database work together.
"""

import sys
import os
import time

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.search_database import SearchDatabase
from tools.serper_search import SerperSearch
from tools.text_extractor import TextExtractor

def demonstrate_workflow():
    """Demonstrate the complete workflow."""

    print("Complete Workflow Example")
    print("=" * 40)
    print("serper_search → text_extractor → database storage")
    print()

    # Initialize components
    db = SearchDatabase()
    serper = SerperSearch()  # This will use API key from environment
    extractor = TextExtractor()

    # Step 1: Perform a search using Serper
    print("Step 1: Performing search with Serper")
    query = "global information trends 2026"

    try:
        search_results = serper.search(query)
        print(f"Found {len(search_results)} results for '{query}'")

        if not search_results:
            print("No results found - this might be due to API limitations or no results")
            return

        # Step 2: Extract text content from the first few results
        print("\nStep 2: Extracting text content")
        extracted_results = []

        # Process only first 3 results for demo purposes
        for i, result in enumerate(search_results[:3]):
            print(f"  Processing result {i+1}: {result['title']}")

            try:
                # Extract content from the URL
                content = extractor.extract_text(result["url"])

                extracted_result = {
                    "url": result["url"],
                    "title": result["title"],
                    "content": content,
                    "search_query": query,
                    "date_posted": None  # Would be extracted from the source if available
                }

                extracted_results.append(extracted_result)
                print(f"    Extracted {len(content)} characters")

                # Add a small delay to be respectful to servers
                time.sleep(1)

            except Exception as e:
                print(f"    Error extracting content: {e}")
                continue

        # Step 3: Store results in database
        print("\nStep 3: Storing results in database")
        if extracted_results:
            stored_count = db.store_results_batch(extracted_results)
            print(f"Successfully stored {stored_count} results")

            # Show database statistics
            stats = db.get_statistics()
            print(f"Database now has {stats['total_results']} total results")

            # Show recent results
            print("\nRecent results in database:")
            recent = db.get_recent_results(2)
            for result in recent:
                print(f"  - {result['title'][:50]}... (from {result['source_domain']})")

        else:
            print("No content was successfully extracted to store")

    except Exception as e:
        print(f"Error in workflow: {e}")
        return

    # Step 4: Demonstrate search capabilities
    print("\nStep 4: Demonstrating database search capabilities")

    # Test searching for specific terms
    search_terms = ["information", "trend", "2026"]
    for term in search_terms:
        results = db.search(term, limit=3)
        print(f"Search for '{term}': found {len(results)} results")

        for result in results[:1]:  # Show first result
            print(f"  - {result['title'][:60]}...")

if __name__ == "__main__":
    demonstrate_workflow()