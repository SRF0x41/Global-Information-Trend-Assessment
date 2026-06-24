#!/usr/bin/env python3
"""
Simple test to verify GDELT client functionality
"""

from gdelt.GDELT_client import GDELTClient
import time


def test_basic_functionality():
    """Test basic GDELT client functionality"""
    print("Testing GDELT Client...")

    client = GDELTClient()

    # Test 1: Basic article search
    print("\n1. Testing basic article search...")
    try:
        result = client.search_articles(
            query="artificial intelligence", maxrecords=5, timespan="1d"
        )
        print("✓ Article search successful")
        print(f"  Found {len(result.get('articles', []))} articles")
    except Exception as e:
        print(f"✗ Article search failed: {e}")

    # Test 2: Timeline analysis
    print("\n2. Testing timeline analysis...")
    try:
        result = client.timeline(
            query="artificial intelligence", timespan="1w", smooth=3
        )
        print("✓ Timeline analysis successful")
        print(f"  Timeline data contains {len(result.get('timeline', []))} time points")
    except Exception as e:
        print(f"✗ Timeline analysis failed: {e}")

    # Test 3: Image gallery (if supported)
    print("\n3. Testing image gallery...")
    try:
        result = client.image_gallery(
            query="artificial intelligence",
            timespan="1w",
            mode="imagegallery",
            maxrecords=5,
        )
        print("✓ Image gallery successful")
        if "images" in result:
            print(f"  Found {len(result['images'])} images")
        else:
            print("  No images found (expected for some queries)")
    except Exception as e:
        print(f"✗ Image gallery failed: {e}")

    print("\n✅ All tests completed!")


if __name__ == "__main__":
    test_basic_functionality()
