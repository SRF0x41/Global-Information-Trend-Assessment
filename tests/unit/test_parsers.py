import pytest
from typing import List, Dict, Any
from parsers.response_parser import ResponseParser
from parsers.tool import Tool


def test_tool_initialization():
    tool_data = {"name": "test_tool", "arguments": {"key": "value"}}
    tool = Tool(tool_data)
    assert tool.get_name() == "test_tool"
    assert tool.get_tool_arguments() == {"key": "value"}
    assert tool.get_raw_json() == tool_data


def test_response_parser_extract_tool_calls():
    parser = ResponseParser()
    text = """
    Here is a tool call:
    <tool_call>{"name": "get_weather", "arguments": {"location": "London"}}</tool_call>
    And another one:
    <tool_call>
    {
        "name": "search",
        "arguments": {"query": "weather in London"}
    }
    </tool_call>
    """
    tool_calls = parser.extract_tool_calls(text)

    assert len(tool_calls) == 2
    assert tool_calls[0].get_name() == "get_weather"
    assert tool_calls[0].get_tool_arguments() == {"location": "London"}
    assert tool_calls[1].get_name() == "search"
    assert tool_calls[1].get_tool_arguments() == {"query": "weather in London"}


def test_response_parser_invalid_json():
    parser = ResponseParser()
    text = "<tool_call>invalid json</tool_call>"
    tool_calls = parser.extract_tool_calls(text)
    assert len(tool_calls) == 0


def test_response_parser_mixed_content():
    parser = ResponseParser()
    text = """
    Some text before <tool_call>{"name": "tool1", "arguments": {}}</tool_call>
    Some text after <tool_call>{"name": "tool2", "arguments": {"a": 1}}</tool_call>
    """
    tool_calls = parser.extract_tool_calls(text)
    assert len(tool_calls) == 2
    assert tool_calls[0].get_name() == "tool1"
    assert tool_calls[1].get_name() == "tool2"
