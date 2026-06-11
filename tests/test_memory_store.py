import unittest
from analysis.memory_store import MemoryStore

class TestMemoryStore(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore()

    def test_add_source(self):
        source_id = self.store.add_source("example.com")
        self.assertGreater(source_id, 0)

    def test_store_document(self):
        source_id = self.store.add_source("test-source")
        doc_id = self.store.store_document(
            source_id=source_id,
            content="Sample document content",
            metadata={"author": "Test User"},
            embedding=np.random.rand(768).astype(np.float32)
        )
        self.assertGreater(doc_id, 0)

    def test_get_document(self):
        source_id = self.store.add_source("test-source")
        doc_id = self.store.store_document(
            source_id=source_id,
            content="Test document",
            metadata={"author": "Test User"},
            embedding=np.random.rand(768).astype(np.float32)
        )

        cursor = self.store.conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[2], "Test document")