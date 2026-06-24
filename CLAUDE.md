# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview
Information Trend Assessment (ITA) is an autonomous, agentic research framework that models the evolving zeitgeist. It identifies patterns, narratives, and tensions across psychological, social, and cultural domains. The system is not a news aggregator — it builds a provisional, revisable model of collective human experience.

The central state is `living_document.md` — the agent's persistent working memory. All operations read from and surgically update this document.

## Architecture & Workflow
The system operates through an iterative agentic loop:

1. **Planning** (`PLAN_PROMPT.md`) — identifies uncertainties, contradictions, blind spots in the Living Document
2. **Search** (`SEARCH_PROMPT.md`) — generates recency-anchored web queries via DuckDuckGo or Serper backends
3. **Extraction** (`EXTRACT_PROMPT.md`) — identifies "signals" (patterns, behaviors, tensions) from gathered content
4. **Comparison** (`COMPARE_PROMPT.md`) — evaluates new signals against existing narratives
5. **Document Update** — surgically updates `living_document.md` via `tools/document_write.py`
6. **Assessment** (`ASSESSMENT_PROMPT.md`) — determines if the model is robust or needs further investigation

### Key Components
- `main.py`: Orchestrator. Currently runs search query generation. Full loop being wired incrementally.
- `living_document.md`: Central evolving state. Contains research priorities, hypotheses, contradictions, blind spots, research plan.
- `original_living_document.md`: Original template reference.
- `reset_living_doc.py`: Backs up current state to timestamped file, resets to initial template.
- `prompts/`: Specialized instructional prompts for each loop step. `SYSTEM_PROMPT.md` is the master persona.
- `tools/`: Agent capabilities — `web_searcher.py` (DuckDuckGo), `serper_search.py` (Google/Serper), `text_extractor.py` (Trafilatura+BS4), `document_write.py` (string-replace document updates).
- `tools/tool_schema/`: Tool cards defining `web_search` and `write` for LLM function calling.
- `llm_clients/lm_studio_client.py`: OpenAI-compatible client defaulting to LM Studio at `http://127.0.0.1:1234/v1`.
- `agent_reasoning/prompt_builder.py`: Token-aware prompt assembly. Supports adding text or file content with automatic truncation.
- `database/search_database.py`: SQLite store for search results with relevance-ranked full-text search.
- `parsers/response_parser.py` + `parsers/tool.py`: Extract tool call JSON blocks from LLM responses.
- `gdelt/GDELT_client.py`: GDELT 2.0 API wrapper for global media monitoring (article search, timeline volume, image gallery).

### Recency Design
All searches are anchored to the present moment. Prompts instruct the model to include recency language (current, latest, this year, right now) in every query. Historical context is gathered only after establishing the current state.

## Development Guide

### Prerequisites
- Python 3.10+

### Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration
Create `.env` with `SERPER_API_KEY=your_key_here`. LLM client defaults to LM Studio on port 1234.

### Common Tasks
- **Running the system:** `python main.py`
- **Resetting state:** `python reset_living_doc.py` (backs up current document, restores template)
- **Testing tools:** `python tools/test_web_searcher.py`
- **Database operations:** `python database/test_database.py`
- **GDELT integration:** `python gdelt/demo_gdelt_integration.py`
- **Managing agent state:** Most operations read and surgically update `living_document.md` via `tools/document_write.py`

### Known Issues
- `serper_search.py:15` — `self.api_key = api_key` references undefined `api_key` parameter (should default to `None`)
- `prompt_builder.py:15` — `encoding_for_model(model)` references undefined `model` variable
- `parsers/tool.py` — missing `from typing import Dict, Any` imports; `get_arguments_named()` references `tool_arguments` without `self.`
