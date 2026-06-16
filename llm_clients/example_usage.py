import logging
from lm_studio_client import LmStudioClient

# Configure logging to see errors if they occur
logging.basicConfig(level=logging.INFO)

def main():
    # 1. Initialize the client
    # Default is http://127.0.0.1:1234/v1
    client = LmStudioClient()

    print("--- LmStudioAPI Example ---")

    # 2. Example: Chat Completion (Standard for instruction-following models)
    print("\n[1] Testing Chat Completions...")
    chat_messages = [
        {"role": "user", "content": "What are the three main pillars of Zeitgeist Intelligence?"}
    ]
    try:
        chat_response = client.chat_completions(messages=chat_messages)
        content = chat_response['choices'][0]['message']['content']
        print(f"Response: {content}")
    except Exception as e:
        print(f"Failed Chat Completion: {e}")

    # # 3. Example: Text Completion (For base/raw text models)
    # print("\n[2] Testing Text Completions...")
    # try:
    #     completion_response = client.completions(prompt="The future of AI is")
    #     text = completion_response['choices'][0]['text']
    #     print(f"Completion: {text.strip()}")
    # except Exception as e:
    #     print(f"Failed Completion: {e}")

    # 4. Example: Embeddings (For vector search/RAG)
    # print("\n[3] Testing Embeddings...")
    # try:
    #     embedding_response = client.embeddings(input="This is a test sentence.")
    #     embedding_vector = embedding_response['data'][0]['embedding']
    #     print(f"Embedding generated successfully! (Vector length: {len(embedding_vector)})")
    # except Exception as e:
    #     print(f"Failed Embeddings: {e}")

if __name__ == "__main__":
    main()
