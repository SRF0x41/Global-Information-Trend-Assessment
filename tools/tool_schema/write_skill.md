## WRITE TOOL — LLM TOOL CARD

### PURPOSE
The `write` tool performs a precise in-place update of a living document used for zeitgeist tracking. It modifies existing text only and does not create new sections.

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
- Must be small, stable, and uniquely identifiable
- Prefer headings, section titles, or fixed markers

value (required)
- Replacement text for the matched target
- Must preserve intent while updating content
- Must reflect updated understanding
- Must not expand scope beyond the target section

---

### WHEN TO USE
Use `write` when:
- Updating existing sections of the living document
- Refining or evolving interpretations or hypotheses
- Merging new signals into existing content
- Correcting outdated or incomplete analysis
- Reordering priorities within existing structure

---

### WHEN NOT TO USE
Do NOT use `write` when:
- No exact target match exists
- A new section must be created
- The correct anchor is uncertain
- Large structural rewrites are required

---

### EDITING RULES
- Make surgical updates only
- Replace, do not append
- Preserve surrounding structure
- Avoid duplication
- Do not modify unintended sections

---

### EXECUTION RULE
If using the tool, output ONLY the <tool_call> block. No explanations or extra text.