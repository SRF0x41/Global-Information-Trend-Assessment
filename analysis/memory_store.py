import sqlite3
import numpy as np
from typing import List, Dict


class MemoryStore:
    def __init__(self, db_path: str = "data/documents.db"):
        self.conn = sqlite3.connect(db_path)
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the database schema if it doesn't exist"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                url TEXT,
                type TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                source_id INTEGER,
                content TEXT,
                metadata TEXT,
                embedding BLOB,
                FOREIGN KEY(source_id) REFERENCES sources(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trends (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                summary TEXT,
                confidence REAL,
                analysis TEXT
            )
        """)

        self.conn.commit()

    def add_source(self, name: str, url: str = None, type: str = "web"):
        """Add a new source to the database"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO sources (name, url, type) VALUES (?, ?, ?)",
            (name, url, type),
        )
        self.conn.commit()
        return cursor.lastrowid

    def store_document(
        self,
        source_id: int,
        content: str,
        metadata: Dict = None,
        embedding: np.ndarray = None,
    ):
        """Store a document with its metadata and optional embedding"""
        cursor = self.conn.cursor()

        # Convert metadata to string for storage
        metadata_str = str(metadata) if metadata else None

        # Convert numpy array to bytes if needed
        embedding_blob = (
            embedding.tobytes() if isinstance(embedding, np.ndarray) else None
        )

        cursor.execute(
            """
            INSERT INTO documents (source_id, content, metadata, embedding)
            VALUES (?, ?, ?, ?)
        """,
            (source_id, content, metadata_str, embedding_blob),
        )

        self.conn.commit()
        return cursor.lastrowid
