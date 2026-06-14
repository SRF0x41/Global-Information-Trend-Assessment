```
# Global Information Trend Assessment (GITA)

## Project Overview
A local-first intelligence and cultural analysis system that:
- Analyzes public internet sources (Reddit, RSS feeds, etc.)
- Tracks emerging cultural and technological trends
- Generates original observations and insights
- Produces recurring zeitgeist reports in markdown format

## Key Features
- **Real-time data collection** from multiple sources
- **Semantic memory system** using FAISS for pattern recognition
- **SQLite-based storage** for structured document metadata
- **Modular architecture** with clear separation of concerns
- **Automated trend detection** and visualization capabilities

## Tech Stack
- Python 3.10+
- SQLite (for structured data)
- FAISS (for semantic similarity search)
- PRAW (Reddit API integration)
- Feedparser (RSS feed handling)
- Requests/BeautifulSoup (web scraping)

## Getting Started
```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python setup.py

# 4. Run tests
test -m pytest tests/
```

## Project Structure
```
gita/
├── data/            # Persistent storage (SQLite, FAISS)
│   └── embeddings.index
├── analysis/        # Core processing modules
│   ├── document_collector.py     # Source data collection
│   ├── trend_analyzer.py         # Pattern recognition
│   ├── memory_store.py           # Storage system
│   └── report_generator.py       # Output generation
├── tests/           # Unit and integration tests
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## System Workflow
1. **Document Collection**
   - `analysis/document_collector.py` gathers content from configured sources
   - Supports Reddit (via PRAW) and RSS feeds (via Feedparser)

2. **Memory Storage**
   - `analysis/memory_store.py` persists data using SQLite
   - Creates FAISS index in `data/embeddings.index`

3. **Trend Analysis**
   - `analysis/trend_analyzer.py` identifies patterns using semantic clustering

4. **Report Generation**
   - `analysis/report_generator.py` produces markdown reports with structured insights

## Documentation
- [CLAUE.md](./CLAUDE.md) contains detailed development instructions for Claude Code users
- [Program Flow Docs](#program-flow-documentation) explain the system architecture in depth

## License
MIT License - See LICENSE file for details
```