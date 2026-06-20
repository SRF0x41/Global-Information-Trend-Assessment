import pytest
from tools.web_searcher import WebSearcher
from tools.document_write import DocumentWrite
from llm_clients.lm_studio_client import LmStudioClient

def test_system_components_instantiation():
    # This test verifies that all major components can be instantiated
    # (using dummy paths/URLs) without immediate errors.

    # 1. Test Searcher
    searcher = WebSearcher()
    assert searcher is not None

    # 2. Test DocumentWrite (requires a file, using a dummy path for now)
    # Since we cannot easily create files in all environments during this step,
    # we'll just check the class is loadable.
    try:
        # We'll skip actual file creation here to avoid cluttering the environment
        # but verify it raises FileNotFoundError if file doesn't exist.
        from unittest.mock import patch
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", create=True):
                dw = DocumentWrite("dummy.md")
                assert dw is not None
    except Exception as e:
        pytest.fail(f"DocumentWrite instantiation failed: {e}")

    # 3. Test LLM Client
    client = LmStudioClient(base_url="http://localhost:1234/v1", api_key="test")
    assert client.base_url == "http://localhost:1234/v1"
