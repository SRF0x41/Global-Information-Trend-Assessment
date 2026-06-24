import pytest
import json


@pytest.fixture
def parser():
    from parsers.response_parser import ResponseParser

    return ResponseParser()


@pytest.fixture
def mock_llm_response():
    return {
        "choices": [
            {
                "message": {
                    "content": '<tool_call>{"name": "search", "arguments": {"q": "weather"}}</tool_call>'
                }
            }
        ]
    }
