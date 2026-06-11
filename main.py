from analysis.document_collector import DocumentCollector
import sqlite3

def main():
    collector = DocumentCollector()

    # Collect and store documents
    conn = sqlite3.connect("data/documents.db")
    cursor = conn.cursor()

    for doc in collector.collect_reddit_posts():
        cursor.execute(
            "INSERT INTO documents (source, content, metadata) VALUES (?, ?, ?)",
            (doc["source"], doc["content"], str(doc["metadata"])))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()