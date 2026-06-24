# Search Database

This directory contains the database implementation for storing search results from the Global Information Trend Assessment system. The database works as a faux search engine, providing flexible search capabilities similar to traditional search engines.

## Purpose

The database serves as persistent storage for:
- Web search results from Serper API
- Extracted text content from URLs
- Search query history and metadata
- Organized knowledge base for trend analysis

## Features

### Database Structure
- **search_results table**: Stores URL, title, content, search query, timestamp, word count, and domain
- **search_queries table**: Tracks search queries and their results
- **Indexes**: Optimized for fast searches on titles, content, URLs, and timestamps

### Search Capabilities
- Flexible text matching (like a search engine)
- Relevance scoring based on term matches in title, content, or URL
- Multi-term search support
- Sorting by relevance and timestamp
- Domain-based filtering

### Key Methods

- `store_result(url, title, content, search_query)`: Store individual results
- `store_results_batch(results)`: Store multiple results efficiently  
- `search(query, limit=20)`: Search through stored content with flexible matching
- `get_result_by_url(url)`: Retrieve specific result by URL
- `get_recent_results(limit)`: Get most recently added results
- `get_statistics()`: Get database statistics

## Usage

```python
from database.search_database import SearchDatabase

# Initialize database
db = SearchDatabase()

# Store a result
db.store_result(
    url="https://example.com/article",
    title="Example Article",
    content="This is the article content...",
    search_query="search terms"
)

# Search results
results = db.search("information trends")
```

## Integration with Tools

The database integrates seamlessly with:
1. `tools.serper_search` - for fetching search results
2. `tools.text_extractor` - for extracting text content from URLs
3. Complete workflow: serper_search → text_extractor → database storage

## Implementation Details

- Uses SQLite for lightweight, file-based storage
- Stores data in a structured format with proper indexing
- Implements rate limiting through delays between operations
- Handles duplicate entries with INSERT OR REPLACE
- Provides comprehensive error handling