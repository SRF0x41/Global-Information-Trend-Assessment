from web_searcher import WebSearcher  # assuming your class is saved here


def main():
    searcher = WebSearcher(timeout=10, max_content_chars=3000)

    query = input("Enter search query: ")

    print("\n Searching...\n")

    results = searcher.search(query, num_results=3)

    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   URL: {r['url']}")
        print(f"   Snippet: {r['snippet']}\n")

    print("\n📄 Fetching full page content...\n")

    detailed = searcher.search_and_read(query, num_results=2)

    for i, r in enumerate(detailed, 1):
        print("=" * 80)
        print(f"PAGE {i}")
        print(f"TITLE: {r['title']}")
        print(f"URL: {r['url']}\n")

        # show preview of content only
        preview = r["content"][:1000]
        print("CONTENT PREVIEW:\n")
        print(preview)
        print("\n")


if __name__ == "__main__":
    main()