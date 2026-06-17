import re
import json
from typing import List, Dict, Any

class ResponseParser:
    """
    Parses response text to extract tool calls.
    """

    def __init__(self):
        self.tool_call_pattern = re.compile(
            r"<tool_call>(.*?)</tool_call>",
            re.DOTALL
        )

    def extract_tool_calls(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract all valid tool call JSON objects.

        Example:

        <tool_call>
        {
            "name": "web_search",
            "arguments": {
                "query": "AI news"
            }
        }
        </tool_call>

        Returns:
        [
            {
                "name": "web_search",
                "arguments": {
                    "query": "AI news"
                }
            }
        ]
        """
        tool_calls = []

        for match in self.tool_call_pattern.findall(text):
            try:
                tool_calls.append(json.loads(match.strip()))
            except json.JSONDecodeError:
                continue

        return tool_calls