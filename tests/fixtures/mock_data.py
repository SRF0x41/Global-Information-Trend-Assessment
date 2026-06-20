import pytest
import requests
from unittest.mock import MagicMock, patch
from llm_clients.lm_studio_client import LmStudioClient

@pytest.fixture
def mock_lm_client():
    with patch("requests.get") as mock_get, patch("requests.post") as mock_post:
        client = LmStudioClient()
        yield client, mock_get, mock_post

MOCK_LLM_RESPONSE_CHATS = {
    "chat_completion_success": {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Here is the plan. <tool_call>{\"name\": \"search\", \"arguments\": {\"query\": \"test\"}}</tool_call>",
                }
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
    }
}
