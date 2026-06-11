import unittest
from analysis.trend_analyzer import TrendAnalyzer
import numpy as np

class TestTrendAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TrendAnalyzer()

    def test_add_embeddings(self):
        # Create some random embeddings
        embeddings = np.random.rand(10, 768).astype(np.float32)

        # Add to index
        self.analyzer.add_embeddings(embeddings)

        # Check that the index has the correct number of vectors
        self.assertEqual(self.analyzer.index.ntotal, 10)

    def test_search_similar(self):
        # Create some random embeddings
        query = np.random.rand(1, 768).astype(np.float32)

        # Add some embeddings to the index
        self.analyzer.add_embeddings(np.random.rand(100, 768).astype(np.float32))

        # Search for similar vectors
        results = self.analyzer.search_similar(query)

        # Check that we got results
        self.assertGreater(len(results), 0)

        # Check that distances are in the expected range
        for distance, _ in results:
            self.assertGreaterEqual(distance, 0.0)