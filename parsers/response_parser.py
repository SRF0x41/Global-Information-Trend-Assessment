import re
import json
from typing import List, Dict, Any
from .tool import Tool

class ResponseParser:
    """
    Parses response text to extract tool calls.
    """

    def __init__(self):
        self.tool_call_pattern = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)

    def extract_tool_calls(self, text: str) -> List[Tool]:
        """
        Extract all valid tool call JSON objects.
        """
        tool_calls = []

        for match in self.tool_call_pattern.findall(text):
            try:
                tool_call = json.loads(match.strip())
                tool_calls.append(Tool(tool_call))

            except json.JSONDecodeError:
                continue

        return tool_calls
