import pytest
import requests
from unittest.mock import MagicMock, patch
from llm_clients.lm_studio_client import LmStudioClient

@pytest.fixture
def client():
    return LmStudioClient(base_url="http://test-api/v1", api_key="test-key")

def test_send_malformed_json(client, monkeypatch):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    monkeypatch.setattr("requests.post", MagicMock(return_value=mock_response))

    # LmStudioClient.send handles exceptions and returns None
    response = client.send(system="You are a helpful assistant", user="Hi")
    assert response is None

def test_send_empty_choices(client, monkeypatch):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"choices": []}
    monkeypatch.setattr("requests.post", MagicMock(return_value=mock_response))

    # Based on the current implementation, if choices is empty, it might raise an IndexError
    # or return None depending on how it's implemented. Let's see if it handles it.
    # If it doesn't, we've found a bug/edge case.
    # The existing test_send_success assumes choices[0].

    # If we want to test the behavior:
    with pytest.raises(IndexError):
        client.send(system="You are a helpful assistant", user="Hi")

def test_send_timeout(client, monkeypatch):
    monkeypatch.setattr("requests.post", MagicMock(side_effect=requests.exceptions.Timeout))

    response = client.send(system="You are a helpful assistant", user="Hi")
    assert response is None
