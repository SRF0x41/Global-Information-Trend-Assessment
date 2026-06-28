# Information Trend Assessment (ITA)

An autonomous, agentic research framework that models the evolving zeitgeist. ITA is not a news aggregator or trend reporter — it is a cultural intelligence system. It gathers evidence, identifies patterns, and then draws bold, grounded conclusions about what those patterns collectively suggest about the human condition right now.

The system reads like a cultural critic who has done the research: it observes, it interprets, and it synthesizes.

## What ITA Does

ITA maintains a **Living Document** — a provisional, revisable model of the present moment. Each research cycle:

1. **Reads the current model** and identifies what's uncertain, contradictory, or incomplete
2. **Gathers new evidence** through recency-anchored web searches
3. **Extracts meaningful signals** — patterns in how people think, feel, behave, and organize
4. **Draws conclusions** — not just summarizing what was found, but answering *"so what does all of this mean?"*

The output is not a report. It's an evolving cultural analysis — the kind of writing that connects a shift in aesthetic taste to a change in how people form communities, then to a deeper psychological tension about identity. The constraint is grounding, not caution.

## The Analytical Lens

ITA observes reality through three interconnected layers:

| Layer | What It Examines |
| :--- | :--- |
| **Psychological** | Emotional patterns, motivations, fears, desires, identity construction, meaning-making, attention, cognition, adaptation |
| **Social** | Collective behavior, group formation, trust systems, social norms, institutions, belonging, status, coordination |
| **Cultural** | Narratives, symbols, aesthetics, rituals, media ecosystems, language shifts, humor, collective myths |

But observation is only the starting point. The system's core task is **synthesis** — weaving signals across these layers into coherent interpretations about the direction of collective human experience.

## Agentic Workflow

```
┌──────────────────────────────────────────────────────────┐
│                    LIVING DOCUMENT STATE                  │
│              (persistent, evolving model)                 │
└────┬─────────────────────────────────────┬───────────────┘
     │                                    │
     ▼                                    ▼
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  PLAN    │ ->│  SEARCH  │ ->│ EXTRACT  │ ->│ UPDATE   │
│ Find     │   │ Gather   │   │ Signals  │   │ Living   │
│ gaps,   │   │ evidence │   │ from     │   │ Document │
│ blind   │   │          │   │ sources  │   │          │
│ spots,  │   │          │   │          │   │          │
│ write   │   │          │   │          │   │          │
│ synthesis│  │          │   │          │   │          │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
     │                                                      │
     │        ┌──────────┐   ┌──────────┐                  │
     └───────│ COMPARE  │ ->│ ASSESS   │──────────────────┘
             │ New vs.  │   │ Model    │  (cycle continues)
             │ existing │   │ robust?  │
             │ narratives│  │          │
             └──────────┘   └──────────┘
```

Each phase does two kinds of work:

| Phase | Mechanical Work | Interpretive Work |
| :--- | :--- | :--- |
| **Plan** | Identify gaps, generate search queries | Write a "Current Synthesis" — what does the model as a whole suggest about this moment? |
| **Search** | Execute recency-anchored queries | Note patterns, contradictions, and surprises that inform next steps |
| **Extract** | Pull signals from sources, ground in evidence | Draw bold conclusions, weave signals into narrative, answer "so what?" |
| **Update** | Surgically edit `living_document.md` | Incorporate insights, revise hypotheses, migrate signals between sections |
| **Refactor** | Transform Living Document into polished report | Produce a cohesive Zeitgeist Report — cultural essay, not a summary |

Note: The Compare and Assess steps are planned but not yet wired into the active flow.

## Core Concept: The Living Document

The Living Document (`living_document.md`) has two zones:

- **Working Notes (Scratchpad)** — Raw observations, half-formed thoughts, tentative connections. Tagged `[UNVERIFIED]`, `[SUPPORTED]`, or `[CONTRADICTED]`.
- **Structured Sections** — Polished, evidence-backed analysis: emerging signals, active narratives, contradictions, blind spots, foundational hypotheses, and **interpretation**.

Signals migrate from scratchpad to structured sections only when multiple independent sources support them. The Interpretation section is where the system answers the big question: *what does all of this collectively suggest?*

## Key Design Principles

- **Recency as baseline** — all searches anchor to the present moment first, then expand backward for historical context
- **Discovery over confirmation** — treat all narratives as hypotheses; actively seek contradictory evidence
- **Synthesis over summary** — don't just report what was found, draw conclusions about what it means
- **Bold but grounded** — creative leaps are expected, but every leap must be traceable back to evidence
- **Signal density over volume** — prefer a few meaningful observations over many weak ones
- **Emergence over taxonomy** — allow explanatory frameworks to emerge from the data, not force observations into predefined categories
- **Behavior over headlines** — observed human behavior is more revealing than stated beliefs or news events
- **Tension over stability** — contradictions are often more revealing than consensus

## System Architecture

```
main.py                          # Orchestrator: search, extract, update, refactor flow
living_document.md               # Central persistent state and working memory
original_living_document.md      # Original template (backup reference)
zeitgeist_report.md              # Polished cultural essay generated from Living Document

prompts/
├── SYSTEM_PROMPT.md             # Master persona, analytical lens, synthesis framework
├── PLAN_PROMPT.md               # Model evaluation, gap analysis, synthesis writing
├── SEARCH_PROMPT.md             # Recency-anchored query generation and execution
├── EXTRACT_PROMPT.md            # Signal extraction, interpretation, narrative synthesis
├── COMPARE_PROMPT.md            # Compare new signals against existing model
├── ASSESSMENT_PROMPT.md         # Model robustness assessment
├── EDIT_PROMPT.md               # Surgical document update instructions
├── REFACTOR_PROMPT.md           # Transform Living Document into Zeitgeist Report
└── GDELT_DOCUMENTATION.md       # GDELT API reference for global media monitoring

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
└── lm_studio_client.py          # OpenAI-compatible client with repeat-loop detection and retry

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

The active flow in `main.py` currently runs: **refactor** — `generate_refactor()` reads the Living Document and produces a polished Zeitgeist Report (`zeitgeist_report.md`). The search → extract → update pipeline is implemented but commented out, ready to be wired back into the full autonomous loop. Compare and Assess steps are planned but not yet implemented.

## Current State

- **Refactor** — `main.py` currently runs `generate_refactor()`, which reads the Living Document and produces a polished Zeitgeist Report (`zeitgeist_report.md`) as a cultural essay
- **Search loop** — generates queries from Living Document gaps, executes via Serper, stores results in SQLite (commented out in main, available for wiring)
- **Extract & Update** — analyzes each article for signals, surgically updates the Living Document (commented out in main, available for wiring)
- **Repeat detection** — LLM client detects and retries on repeat loops in streaming output
- **Planned** — Compare (new vs existing narratives), Assess (model robustness), full autonomous loop with planning wired back in

## Contributing

This is an experimental research framework. Contributions are welcome in the form of:

- Improvements to prompt engineering
- Expansion of analytical frameworks
- Enhancements to search strategies
- Development of new tools for analysis
