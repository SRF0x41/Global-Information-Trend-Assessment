import pytest
import requests
from unittest.mock import MagicMock, patch
from llm_clients.lm_studio_client import LmStudioClient


@pytest.fixture
def client():
    return LmStudioClient(base_url="http://test-api/v1", api_key="test-key")


def test_lm_studio_client_init(client):
    assert client.base_url == "http://test-api/v1"
    assert client.api_key == "test-key"
    assert client.timeout is None


def test_get_headers(client):
    headers = client._get_headers()
    assert headers["Authorization"] == "Bearer test-key"
    assert headers["Content-Type"] == "application/json"


def test_list_models_success(client, monkeypatch):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": "model-1"}]}
    monkeypatch.setattr("requests.get", MagicMock(return_value=mock_response))

    result = client.list_models()
    assert result["data"][0]["id"] == "model-1"


def test_list_models_error(client, monkeypatch):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Not Found"
    )
    monkeypatch.setattr("requests.get", MagicMock(return_value=mock_response))

    with pytest.raises(requests.exceptions.HTTPError):
        client.list_models()


def test_send_success(client, monkeypatch):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Hello there!"}}]
    }
    monkeypatch.setattr("requests.post", MagicMock(return_value=mock_response))

    response = client.send(system="You are a helpful assistant", user="Hi")
    assert response == "Hello there!"


def test_send_failure(client, monkeypatch):
    # Simulate an exception in chat_completions
    monkeypatch.setattr(
        "requests.post", MagicMock(side_effect=Exception("Connection error"))
    )

    response = client.send(system="You are a helpful assistant", user="Hi")
    assert response is None


def test_chat_completions_payload(client, monkeypatch):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"choices": []}
    post_mock = MagicMock(return_value=mock_response)
    monkeypatch.setattr("requests.post", post_mock)

    client.chat_completions(
        messages=[{"role": "user", "content": "test"}], temperature=0.7, max_tokens=100
    )

    args, kwargs = post_mock.call_args
    assert kwargs["json"]["temperature"] == 0.7
    assert kwargs["json"]["max_tokens"] == 100
    # The model parameter should be filtered out when None (as per implementation)
    assert "model" not in kwargs["json"]


def test_embeddings_success(client, monkeypatch):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"embedding": [0.1, 0.2]}]}
    monkeypatch.setattr("requests.post", MagicMock(return_value=mock_response))

    result = client.embeddings(input="hello")
    assert "data" in result
    assert result["data"][0]["embedding"] == [0.1, 0.2]
