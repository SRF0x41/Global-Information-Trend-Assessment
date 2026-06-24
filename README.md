# Global Information Trend Assessment (GITA)

An autonomous, agentic research framework designed to model the evolving global zeitgeist. Rather than summarizing news, the system identifies patterns, narratives, and tensions across psychological, social, and cultural domains to build a multidimensional model of the present moment.

## Core Concept: The Living Document

At the heart of the system is the **Living Document** (`living_document.md`). This document serves as the agent's persistent, evolving working memory. The agent does not collect articles — it synthesizes information into a coherent, provisional model of reality, continuously revising itself as new evidence arrives.

The analytical lens operates through three interconnected layers:

| Layer | Focus Areas |
| :--- | :--- |
| **Psychological** | Emotional patterns, motivations, fears, desires, identity construction, meaning-making, attention, cognition |
| **Social** | Collective behavior, group formation, trust systems, social norms, institutions, belonging, status |
| **Cultural** | Narratives, symbols, aesthetics, rituals, media ecosystems, language shifts, humor, collective myths |

## Agentic Workflow

The system operates through a continuous, iterative loop:

1. **Planning** — Identifies uncertainties, contradictions, and blind spots in the Living Document. Proposes research directions that could materially change the model.
2. **Search** — Executes targeted web searches (via DuckDuckGo or Serper) anchored to the present moment, with recency language to prioritize recent signals.
3. **Extraction** — Processes gathered content to identify "signals" — recurring patterns, behaviors, tensions — rather than mere summaries.
4. **Comparison** — Evaluates new signals against existing narratives. Does new evidence support, weaken, or contradict the current model?
5. **Document Update** — Surgically updates the Living Document with validated signals and revised hypotheses.
6. **Assessment** — Determines if the current model is robust or requires further investigation.

## System Architecture

```
main.py                          # Orchestrator: planning, search, extract loop
living_document.md               # Central persistent state and working memory
original_living_document.md      # Original template (backup reference)

prompts/
├── SYSTEM_PROMPT.md             # Master persona: cultural analyst / zeitgeist interpreter
├── PLAN_PROMPT.md               # Planning layer: identify gaps, propose research
├── SEARCH_PROMPT.md             # Search layer: recency-anchored query generation
├── EXTRACT_PROMPT.md            # Extraction layer: signal identification from sources
├── COMPARE_PROMPT.md            # Comparison layer: new vs existing narratives
├── ASSESSMENT_PROMPT.md         # Assessment layer: model robustness check
├── EDIT_PROMPT.md               # Document editing instructions
└── GDELT_DOCUMENTATION.md       # GDELT API reference

tools/
├── web_searcher.py              # DuckDuckGo search + page reader
├── serper_search.py             # Serper (Google) search backend
├── text_extractor.py            # Trafilatura + BeautifulSoup content extraction
├── document_write.py            # Surgical string-replacement document updates
├── tool_schema/                 # Tool cards for LLM function calling
│   ├── web_searcher_skill.md    # web_search tool definition
│   └── write_skill.md           # write tool definition
└── tools_schema.md              # Consolidated tool schema reference

llm_clients/
└── lm_studio_client.py          # OpenAI-compatible client (LM Studio, local models)

agent_reasoning/
└── prompt_builder.py            # Token-aware prompt assembly with file/text components

database/
└── search_database.py           # SQLite store for search results with full-text search

parsers/
├── response_parser.py           # Extracts tool calls from LLM responses
└── tool.py                      # Tool call representation

gdelt/
├── GDELT_client.py              # GDELT 2.0 API wrapper (global media monitoring)
├── demo_gdelt_integration.py    # Example GDELT integration flow
└── test_gdelt_client.py         # GDELT client tests

tests/
├── conftest.py                  # Pytest configuration
├── unit/                        # Unit tests
└── integration/                 # Integration tests

reset_living_doc.py              # Backup + reset Living Document to initial template
```

## Getting Started

### Prerequisites
- Python 3.10+
- Local LLM server (LM Studio) or compatible OpenAI-compatible API endpoint

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file with your API keys:

```
SERPER_API_KEY=your_serper_api_key_here
```

The LLM client defaults to `http://127.0.0.1:1234/v1` (LM Studio). Modify `LmStudioClient` in `llm_clients/lm_studio_client.py` to point to a different endpoint.

### Usage

```bash
python main.py
```

Currently `main.py` runs the search query generation loop. The full agentic cycle (plan → search → extract → compare → assess) is being wired up incrementally.

## Key Design Principles

- **Recency as baseline** — all searches anchor to the present moment first, then expand backward when historical context is needed
- **Discovery over confirmation** — treat all narratives as hypotheses; actively seek contradictory evidence
- **Signal density over volume** — prefer a few meaningful observations over many weak ones
- **Emergence over taxonomy** — do not force observations into predefined categories; allow explanatory frameworks to emerge from the data
- **Behavior over headlines** — observed human behavior is more revealing than stated beliefs or news events

## Roadmap

- **Full agentic loop** — wire up the complete plan → search → extract → compare → refactor → assess cycle
- **GDELT integration** — incorporate global media monitoring for cross-regional signal detection
- **Primary source analysis** — analyze trending media, social posts, and cultural artifacts for organic sentiment
- **Automated assessment loops** — trigger deeper investigations when conflicting signals are detected
- **Enhanced tool integration** — expand data sources and analysis methods

## Contributing

This is an experimental research framework. Contributions are welcome in the form of:

- Improvements to prompt engineering
- Expansion of analytical frameworks
- Enhancements to search strategies
- Development of new tools for analysis
