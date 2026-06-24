from parsers.tool import Tool


def test_tool_initialization():
    tool_call = {"name": "search", "arguments": {"query": "climate change"}}
    tool = Tool(tool_call)
    assert tool.get_name() == "search"
    assert tool.get_tool_arguments() == {"query": "climate change"}
    assert tool.get_raw_json() == tool_call


def test_tool_with_missing_arguments():
    tool_call = {"name": "search"}
    tool = Tool(tool_call)
    assert tool.get_tool_arguments() == {}


def test_tool_with_extra_fields():
    tool_call = {
        "name": "search",
        "arguments": {"query": "climate change"},
        "id": "123",
    }
    tool = Tool(tool_call)
    assert tool.get_name() == "search"
    assert tool.get_tool_arguments() == {"query": "climate change"}
    assert tool.get_raw_json() == tool_call
