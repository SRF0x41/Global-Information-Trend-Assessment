import json
import os
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import sqlite3
from pathlib import Path


class SearchDatabase:
    """
    Database system for storing search results with search engine-like capabilities.
    This faux search engine stores web content and allows flexible searching.
    """

    def __init__(self, db_path: str = "database/search_results.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database and create tables if they don't exist."""
        # Create directory if it doesn't exist
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create table for search results
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                content TEXT NOT NULL,
                search_query TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                word_count INTEGER,
                source_domain TEXT,
                date_posted TEXT
            )
        """)

        # Create table for search queries
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                result_count INTEGER
            )
        """)

        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON search_results(title)")
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_content ON search_results(content)"
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_url ON search_results(url)")
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_search_query ON search_results(search_query)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_timestamp ON search_results(timestamp)"
        )

        conn.commit()
        conn.close()

    def store_result(
        self,
        url: str,
        title: str,
        content: str,
        search_query: str = None,
        date_posted: str = None,
    ) -> bool:
        """
        Store a search result in the database.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Extract domain from URL
            domain = self._extract_domain(url)

            # Calculate word count
            word_count = len(content.split())

            # Insert or update the result
            cursor.execute(
                """
                INSERT OR REPLACE INTO search_results
                (url, title, content, search_query, word_count, source_domain, date_posted)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (url, title, content, search_query, word_count, domain, date_posted),
            )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error storing result: {e}")
            return False

    def store_results_batch(self, results: List[Dict[str, Any]]) -> int:
        """
        Store multiple search results in batch.
        """
        stored_count = 0
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for result in results:
                url = result.get("url", "")
                title = result.get("title", "")
                content = result.get("content", "")
                search_query = result.get("search_query", "")
                date_posted = result.get("date_posted", None)

                # Extract domain from URL
                domain = self._extract_domain(url)

                # Calculate word count
                word_count = len(content.split())

                cursor.execute(
                    """
                    INSERT OR REPLACE INTO search_results
                    (url, title, content, search_query, word_count, source_domain, date_posted)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        url,
                        title,
                        content,
                        search_query,
                        word_count,
                        domain,
                        date_posted,
                    ),
                )

                stored_count += 1

            conn.commit()
            conn.close()
            return stored_count

        except Exception as e:
            print(f"Error storing batch results: {e}")
            return stored_count

    def search(
        self, query: str, limit: int = 20, min_relevance: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Search through stored content with flexible matching (like a search engine).
        Returns results sorted by relevance.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Simple full-text search with ranking
            search_terms = query.lower().split()

            # Build a flexible search query that matches content, title, or URL
            if len(search_terms) == 1:
                # Single term search - look in title, content, and URL
                cursor.execute(
                    """
                    SELECT *,
                           (CASE WHEN title LIKE ? THEN 10 ELSE 0 END +
                            CASE WHEN content LIKE ? THEN 5 ELSE 0 END +
                            CASE WHEN url LIKE ? THEN 3 ELSE 0 END) as relevance_score
                    FROM search_results
                    WHERE title LIKE ? OR content LIKE ? OR url LIKE ?
                    ORDER BY relevance_score DESC, timestamp DESC
                    LIMIT ?
                """,
                    (
                        f"%{search_terms[0]}%",
                        f"%{search_terms[0]}%",
                        f"%{search_terms[0]}%",
                        f"%{search_terms[0]}%",
                        f"%{search_terms[0]}%",
                        f"%{search_terms[0]}%",
                        limit,
                    ),
                )
            else:
                # Multi-term search - look for any of the terms
                placeholders = ", ".join(["?" for _ in search_terms])
                search_conditions = " OR ".join(
                    [
                        "title LIKE ? OR content LIKE ? OR url LIKE ?"
                        for _ in search_terms
                    ]
                )

                # Prepare all parameters
                params = []
                for term in search_terms:
                    params.extend([f"%{term}%", f"%{term}%", f"%{term}%"])

                params.append(limit)

                cursor.execute(
                    f"""
                    SELECT *,
                           (CASE WHEN title LIKE ? THEN 10 ELSE 0 END +
                            CASE WHEN content LIKE ? THEN 5 ELSE 0 END +
                            CASE WHEN url LIKE ? THEN 3 ELSE 0 END) as relevance_score
                    FROM search_results
                    WHERE {search_conditions}
                    ORDER BY relevance_score DESC, timestamp DESC
                    LIMIT ?
                """,
                    params,
                )

            rows = cursor.fetchall()
            conn.close()

            # Convert to list of dictionaries
            results = []
            for row in rows:
                result = dict(row)
                # Remove the internal relevance_score field from display
                if "relevance_score" in result:
                    del result["relevance_score"]
                results.append(result)

            return results

        except Exception as e:
            print(f"Error performing search: {e}")
            return []

    def get_result_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific result by URL.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM search_results WHERE url = ?
            """,
                (url,),
            )

            row = cursor.fetchone()
            conn.close()

            if row:
                return dict(row)
            return None

        except Exception as e:
            print(f"Error retrieving result: {e}")
            return None

    def get_recent_results(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recently added results.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM search_results
                ORDER BY timestamp DESC
                LIMIT ?
            """,
                (limit,),
            )

            rows = cursor.fetchall()
            conn.close()

            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error retrieving recent results: {e}")
            return []

    def get_results_by_query(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get results that were searched with a specific query.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM search_results
                WHERE search_query LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            """,
                (f"%{query}%", limit),
            )

            rows = cursor.fetchall()
            conn.close()

            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error retrieving query results: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Count total results
            cursor.execute("SELECT COUNT(*) as total FROM search_results")
            total = cursor.fetchone()[0]

            # Count unique domains
            cursor.execute(
                "SELECT COUNT(DISTINCT source_domain) as domains FROM search_results"
            )
            domains = cursor.fetchone()[0]

            # Get latest timestamp
            cursor.execute("SELECT MAX(timestamp) as latest FROM search_results")
            latest = cursor.fetchone()[0]

            conn.close()

            return {
                "total_results": total,
                "unique_domains": domains,
                "latest_timestamp": latest,
            }

        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}

    def _extract_domain(self, url: str) -> str:
        """
        Extract domain from URL.
        """
        try:
            from urllib.parse import urlparse

            parsed_url = urlparse(url)
            return parsed_url.netloc
        except:
            return ""

    def delete_result_by_url(self, url: str) -> bool:
        """
        Delete a specific result by URL.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM search_results WHERE url = ?", (url,))
            deleted = cursor.rowcount > 0

            conn.commit()
            conn.close()
            return deleted

        except Exception as e:
            print(f"Error deleting result: {e}")
            return False

    def clear_database(self) -> bool:
        """
        Clear all results from the database.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM search_results")
            cursor.execute("DELETE FROM search_queries")

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error clearing database: {e}")
            return False
