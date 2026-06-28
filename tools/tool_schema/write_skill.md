## WRITE TOOL — LLM TOOL CARD

### PURPOSE
The `write` tool performs surgical updates to the living document used for zeitgeist tracking.
---

### MODE 1 — Section-based (RECOMMENDED)

Target a section by its header name. This is the most reliable mode — header names are short and stable.

<tool_call>
{
  "name": "write",
  "arguments": {
    "section": "EMERGING SIGNALS",
    "operation": "append",
    "content": "## New Signal\n\nDescription of the signal..."
  }
}
</tool_call>

**Arguments**

| Field       | Required | Description                                                    |
|-------------|----------|----------------------------------------------------------------|
| `section`   | yes      | Exact section header text (e.g. `EMERGING SIGNALS`, `BLIND SPOTS`) |
| `operation` | yes      | `append` — add to end of section body. `replace` — swap entire section body. `create` — write content as the initial document (use when file is empty/missing). |
| `content`   | yes      | Markdown text to insert or replace with.                        |

**When to use**
- Adding new signals, narratives, contradictions, blind spots, hypotheses
- Replacing an entire section with an updated version
- Most document updates

---

### MODE 2 — Target-based (fallback)

Replace an exact string in the document. Use only when you need to change a specific line or phrase inside a section.

<tool_call>
{
  "name": "write",
  "arguments": {
    "target": "Current State: Initial",
    "value": "Current State: Updated"
  }
}
</tool_call>
**Arguments**

| Field    | Required | Description                                      |
|----------|----------|--------------------------------------------------|
| `target` | yes      | Exact text to find in the document.               |
| `value`  | yes      | Replacement text. Use `""` to delete the target.  |

**Note:** If `target` has a small typo (90%+ similar), fuzzy matching will find the closest match automatically.

---

### MODE 3 — Append (quick add)

Omit `section` and `target` to append content to the end of the document.

<tool_call>
{
  "name": "write",
  "arguments": {
    "value": "New content appended to end of document."
  }
}
</tool_call>

---

### EDITING RULES
- Prefer **Mode 1 (section-based)** — it's more reliable than quoting long text.
- Make surgical updates only — don't touch unrelated sections.
- Avoid duplication.
- One `write` tool call per update.

### EXECUTION RULE
If using the tool, output ONLY the `<tool_call>` block. No explanations or extra text.
