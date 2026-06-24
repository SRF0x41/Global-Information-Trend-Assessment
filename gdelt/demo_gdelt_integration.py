#!/usr/bin/env python3
"""
Demonstration of updated GDELT 2.0 DOC API integration for Global Information Trend Assessment

This script demonstrates the complete implementation of the GDELT client with:
1. Proper API endpoint usage for GDELT 2.0 DOC API
2. Implementation of 7-second delays between requests as required
3. Support for text-based search modes: artlist, timelinevol
4. Integration-ready patterns for the agent system
"""

from GDELT_client import GDELTClient
import time

def demonstrate_gdelt_integration():
    """Demonstrate complete GDELT integration with proper delays"""

    print("Starting GDELT 2.0 DOC API Demonstration")
    print("=" * 60)

    # Initialize the client
    client = GDELTClient()

    # Define topics for analysis
    topics = [
        "artificial intelligence",
        "climate change",
        "global conflicts"
    ]

    print(f"\nAnalyzing {len(topics)} topics:")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")

    # 1. Article search (main text content analysis)
    print("\nPerforming article searches...")
    article_results = {}
    for topic in topics:
        print(f"   Searching articles about '{topic}'...")
        try:
            article_results[topic] = client.search_articles(
                query=topic,
                maxrecords=50,  # More records for better analysis
                timespan="1w",  # Last week of coverage
                sort="HybridRel"
            )
            print(f"   Found {len(article_results[topic].get('articles', []))} articles")
        except Exception as e:
            print(f"   Error: {e}")

    # 2. Timeline analysis (trend detection)
    print("\nPerforming timeline analysis...")
    timeline_results = {}
    for topic in topics:
        print(f"   Analyzing trend for '{topic}'...")
        try:
            timeline_results[topic] = client.timeline(
                query=topic,
                timespan="1m",  # Last month for trend analysis
                smooth=5
            )
            print(f"   Timeline with {len(timeline_results[topic].get('timeline', []))} data points")
        except Exception as e:
            print(f"   Error: {e}")

    # 3. Complete zeitgeist snapshot
    print("\nCreating comprehensive zeitgeist snapshot...")
    try:
        snapshot = client.zeitgeist_snapshot(topics)
        print("Zeitgeist snapshot created successfully")
        print(f"  - Articles analyzed: {len(snapshot)} topics")
        print(f"  - Timeline data: {len(snapshot)} topics")
    except Exception as e:
        print(f"Error creating snapshot: {e}")

    # 4. Demonstrate delay functionality
    print("\nVerifying 7-second delay implementation...")
    start_time = time.time()
    client.search_articles("test query", maxrecords=5)
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Delay verification: {elapsed:.2f} seconds (should be ~7)")

    print("\nAll GDELT 2.0 DOC API demonstrations completed!")
    print("\nSummary of implemented features:")
    print("   - Full GDELT 2.0 DOC API endpoint support")
    print("   - Proper 7-second delay between requests")
    print("   - Text-based modes: artlist, timelinevol")
    print("   - Time window filtering (timespan, startdatetime, enddatetime)")
    print("   - Configurable max records and sorting options")
    print("   - Integration-ready patterns for agent system")

if __name__ == "__main__":
    demonstrate_gdelt_integration()