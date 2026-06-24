#!/usr/bin/env python3
"""
Sample usage of the TextExtractor tool for the Global Information Trend Assessment system.
This file demonstrates various ways to use the TextExtractor class.
"""

import os
from tools.text_extractor import TextExtractor

def main():
    # Initialize the text extractor
    extractor = TextExtractor()

    print("Text Extractor Usage Examples")
    print("=" * 40)

    # Example 1: Extract text from a single URL
    print("\n1. Single URL Extraction:")
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    try:
        content = extractor.extract_text(url)
        print(f"Extracted {len(content)} characters from {url}")
        print(f"First 200 characters: {content[:200]}...")
    except Exception as e:
        print(f"Error extracting text: {e}")

    # Example 2: Extract with metadata
    print("\n2. Extraction with Metadata:")
    try:
        result = extractor.extract_with_metadata(url)
        print(f"URL: {result['url']}")
        print(f"Title: {result['title']}")
        print(f"Content length: {len(result['content'])} characters")
        print(f"Processing time: {result['elapsed_seconds']} seconds")
    except Exception as e:
        print(f"Error with metadata extraction: {e}")

    # Example 3: Batch extraction
    print("\n3. Batch Extraction:")
    urls = [
        "https://en.wikipedia.org/wiki/Machine_learning",
        "https://en.wikipedia.org/wiki/Deep_learning",
        "https://en.wikipedia.org/wiki/Natural_language_processing"
    ]

    try:
        results = extractor.batch_extract(urls)
        for i, result in enumerate(results):
            print(f"Result {i+1}: {result['url']} ({len(result['content'])} chars)")
    except Exception as e:
        print(f"Error in batch extraction: {e}")

    # Example 4: Handling invalid URLs
    print("\n4. Error Handling:")
    invalid_url = "https://this-domain-does-not-exist-12345.com"
    try:
        content = extractor.extract_text(invalid_url)
        print(f"Content from invalid URL: {content}")
    except Exception as e:
        print(f"Error with invalid URL: {e}")

if __name__ == "__main__":
    main()