import pytest
import requests
from unittest.mock import MagicMock, patch
from llm_clients.lm_studio_client import LmStudioClient

@pytest.fixture
def lm_client():
    return LmStudioClient(base_url="http://localhost:1234/v1")

def test_send_success(lm_client, mocker):
    mock_post = mocker.patch("requests.post")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Hello from LLM"}}]
    }
    mock_post.return_value = mock_response

    content = lm_client.send(system="You are a helpful assistant", user="Hi")

    assert content == "Hello from LLM"
    assert mock_post.called

def test_send_error_500(lm_client, mocker):
    mock_post = mocker.patch("requests.post")
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    mock_post.return_value = mock_response

    # The send method catches exceptions and returns None
    content = lm_client.send(system="System", user="User")
    assert content is None

def test_send_malformed_json(lm_client, mocker):
    mock_post = mocker.patch("requests.post")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_post.return_value = mock_response

    # The send method catches exceptions and returns None
    content = lm_client.send(system="System", user="User")
    assert content is None

def test_send_empty_content(lm_client, mocker):
    mock_post = mocker.patch("requests.post")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": ""}}]
    }
    mock_post.return_value = mock_response

    content = lm_client.send(system="System", user="User")
    assert content == ""
