import pytest
from unittest.mock import MagicMock, patch
from tools.web_searcher import WebSearcher
import requests

@pytest.fixture
def searcher():
    return WebSearcher()

@patch("requests.Session.get")
def test_full_search_and_read_integration(mock_get, searcher):
    # 1. Mock Search Response
    search_response = MagicMock()
    search_response.status_code = 200
    search_response.text = """
    <div class="result">
        <a class="result__a" href="//duckduckgo.com/?uddg=https%3A%2F%2Fexample.com&q=test">Title 1</a>
        <div class="result__snippet">Snippet 1</div>
    </div>
    <div class="result">
        <a class="result__a" href="//duckduckgo.com/?uddg=https%3A%2F%2Fexample.org&q=test">Title 2</a>
        <div class="result__snippet">Snippet 2</div>
    </div>
    """
    search_response.raise_for_status.return_value = None

    # 2. Mock Page Fetch Responses
    page1_response = MagicMock()
    page1_response.status_code = 200
    page1_response.text = "Content from example.com"
    page1_response.raise_for_status.return_value = None

    page2_response = MagicMock()
    page2_response.status_code = 200
    page2_response.text = "Content from example.org"
    page2_response.raise_for_status.return_value = None

    # Sequence of responses for the multiple calls in search_and_read
    mock_get.side_effect = [search_response, page1_response, page2_response]

    # Execute
    results = searcher.search_and_read("test", num_results=2)

    # Assert
    assert len(results) == 2
    assert results[0]["title"] == "Title 1"
    assert results[0]["content"] == "Content from example.com"
    assert results[1]["title"] == "Title 2"
    assert results[1]["content"] == "Content from example.org"
