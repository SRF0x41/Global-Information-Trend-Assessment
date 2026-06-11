import faiss
import numpy as np
from typing import List, Dict

class TrendAnalyzer:
    def __init__(self, index_path: str = "data/embeddings.index"):
        self.index_path = index_path
        self.index = None
        self.load_index()

    def load_index(self):
        """Load FAISS index from disk"""
        if faiss.is_available():
            self.index = faiss.read_index(self.index_path)
        else:
            raise RuntimeError("FAISS is not available")

    def add_embeddings(self, embeddings: np.ndarray):
        """Add new embeddings to the index"""
        if self.index is None:
            # Create a new index if it doesn't exist
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)
        faiss.write_index(self.index, self.index_path)

    def search_similar(self, query_embedding: np.ndarray, k: int = 5):
        """Find similar embeddings in the index"""
        if self.index is None:
            return []

        distances, indices = self.index.search(query_embedding, k)
        return list(zip(distances[0], indices[0]))