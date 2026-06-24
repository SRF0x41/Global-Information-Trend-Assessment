## WRITE TOOL — LLM TOOL CARD

### PURPOSE
The `write` tool performs updates of a living document used for zeitgeist tracking. 
---

### TOOL CALL FORMAT
<tool_call>
{
  "name": "write",
  "arguments": {
    "target": "string",
    "value": "string"
  }
}
</tool_call>

---

### ARGUMENTS

target (required)
- Exact string match from the document (first occurrence is replaced)

value (required)
- Replacement text for the matched target

---

### WHEN TO USE
Use `write` when:
- Updating existing sections of the living document

---

### EDITING RULES
- Make surgical updates only
- Avoid duplication
- Do not modify unintended sections

### APPEND NEW CONTENT (append mode)

Use this when adding new content to the document.

### IMPORTANT:
Appending is done by omitting target. There is no separate append tool.

### APPENDING INFORMATION
<tool_call>
{
  "name": "write",
  "arguments": {
    "value": "string"
  }
}
</tool_call>

---

### DELETING SECTIONS OF TEXT
If you need to delete sections of information, replace the target with an empty string in the value parameter.


### EXECUTION RULE
If using the tool, output ONLY the <tool_call> block. No explanations or extra text.