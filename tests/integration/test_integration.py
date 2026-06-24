import pytest
from unittest.mock import MagicMock, patch
from llm_clients.lm_studio_client import LmStudioClient
from parsers.response_parser import ResponseParser


def test_full_flow_mocked(parser, mock_llm_response):
    # This simulates a piece of the agent loop:
    # 1. Get response from LLM (mocked)
    # 2. Parse the response for tool calls

    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_llm_response
        mock_post.return_value = mock_response

        client = LmStudioClient(base_url="http://localhost:1234/v1")

        # Step 1: Get content
        content = client.send(system="You are an agent", user="Search for weather")

        # Step 2: Parse tool calls
        tool_calls = parser.extract_tool_calls(content)

        assert len(tool_calls) == 1
        assert tool_calls[0].get_name() == "search"
        assert tool_calls[0].get_tool_arguments() == {"q": "weather"}
