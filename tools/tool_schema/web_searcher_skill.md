## WEB SEARCHER TOOL — LLM TOOL CARD

### PURPOSE
The `web_search` tool performs targeted web searches to gather external signals for zeitgeist analysis. It uses DuckDuckGo to find relevant content and extracts full page text for detailed analysis.

---
### TOOL CALL FORMAT
<tool_call>
{
  "name": "web_search",
  "arguments": {
    "query": "string",
  }
}
</tool_call>

---

### ARGUMENTS

query (required)
- The search query string to use for finding relevant web content
- Should be specific and focused on psychological, social, or cultural phenomena
- Must include context from the living document state


---

### WHEN TO USE
Use `web_search` when:
- Conducting research to support the planning phase
- Gathering evidence for extracting signals from content
- Expanding on weak signals identified in the living document
- Testing contradictions between existing narratives and new findings

---

### SEARCH GUIDELINES
- Queries should focus on behavioral patterns rather than news events
- Include relevant context from the current living document state
- Phrase queries to reveal underlying trends rather than surface events
- Prioritize sources that show real-world behavioral patterns over just news reports
- Use terms that capture collective human experience and behavior

---

### OUTPUT FORMAT
The tool returns search results in this format:
- title: The page title
- url: The web address
- snippet: A brief excerpt from the page
- content: The full extracted text content (if available)

---

### EXECUTION RULE
If using the tool, output ONLY the JSON block. No explanations or extra text.