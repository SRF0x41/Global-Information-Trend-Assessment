class Tool:

    def __init__(self, tool_call: Dict[str, Any]):
        """Take the entire json and parse here"""
        # Store the most recently parsed tool call
        self.raw_json = tool_call
        self.tool_name = tool_call.get("name")
        self.tool_arguments = tool_call.get("arguments", {})

    def get_name(self):
        return self.tool_name

    def get_tool_arguments(self):
        return self.tool_arguments

    def get_raw_json(self):
        return self.raw_json

    def get_arguments_named(self):
        return list(self.tool_arguments)
