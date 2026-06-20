import pytest
from parsers.response_parser import ResponseParser
from parsers.tool import Tool

@pytest.fixture
def parser():
    return ResponseParser()

def test_extract_tool_calls_success(parser):
    text = "<tool_call>{\"name\": \"get_weather\", \"arguments\": {\"location\": \"London\"}}</tool_call>"
    tool_calls = parser.extract_tool_calls(text)

    assert len(tool_calls) == 1
    assert isinstance(tool_calls[0], Tool)
    assert tool_calls[0].get_name() == "get_weather"
    assert tool_calls[0].get_tool_arguments() == {"location": "London"}

def test_extract_tool_calls_multiple(parser):
    text = """
    Here is the tool call:
    <tool_call>{"name": "tool1", "arguments": {}}</tool_call>
    And another:
    <tool_call>{"name": "tool2", "arguments": {"arg": 1}}</tool_call>
    """
    tool_calls = parser.extract_tool_calls(text)

    assert len(tool_calls) == 2
    assert tool_calls[0].get_name() == "tool1"
    assert tool_calls[1].get_name() == "tool2"

def test_extract_tool_calls_invalid_json(parser):
    text = "<tool_call>{\"name\": \"tool1\", \"arguments\": {incomplete_json}}</tool_call>"
    tool_calls = parser.extract_tool_calls(text)

    assert len(tool_calls) == 0

def test_extract_tool_calls_no_match(parser):
    text = "Just some text without tool calls."
    tool_calls = parser.extract_tool_calls(text)

    assert len(tool_calls) == 0

def test_extract_tool_calls_malformed_tags(parser):
    text = "<tool_call>{\"name\": \"tool1\"} /tool_call>"
    tool_calls = parser.extract_tool_calls(text)

    assert len(tool_calls) == 0
