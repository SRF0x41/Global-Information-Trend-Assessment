# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Global Information Trend Assessment is an autonomous, agentic research framework designed to monitor, synthesize, and model the evolving global zeitgeist. It focuses on identifying patterns, narratives, and tensions across multiple domains (Cultural, Technological, Economic, Political, Social, and Psychological) rather than just summarizing news.

The system is built around a "Living Document" (`living_document.md`) which acts as the agent's persistent, evolving working memory and state.

## Architecture & Workflow
The system operates through a continuous, iterative loop of specialized agentic tasks:

1.  **Planning:** Formulates research strategies and identifies information gaps based on the current state of the `living_document.md`.
2.  **Search:** Uses `web_search` to gather external signals via web search tools.
3.  **Extraction:** Processes information to identify "signals" (patterns, themes, or tensions) and updates the `living_document.md`.
4.  **Comparison:** Evaluates new signals to see if they support, weaken, or contradict existing narratives in the document.
5.  **Refactoring:** Continuously refines the `living_document.md` for human readability and coherence.
6.  **Assessment:** Determines if the current model is robust or requires further investigation.

### Key Components
- `main.py`: The entry point for the agentic loop (currently a skeleton).
- `living_document.md`: The central, evolving state of the system and primary working memory.
- `prompts/`: Contains specialized instructional prompts for each step of the agentic loop (e.g., `PLAN_PROMPT.md`, `SEARCH_PROMPT.md`, etc.).
- `tools/`: Contains the agent's capabilities (e.g., `web_searcher.py`, `document_write.py`).
- `requirements.txt`: Python dependencies.

## Development Guide

### Prerequisites
- Python 3.10+

### Installation
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Common Tasks
- **Running the system:** `python main.py` (Note: `main.py` is currently a skeleton).
- **Testing tools:** Manual test scripts are available, e.g., `python tools/test_web_searcher.py`.
- **Managing the agent's state:** Most operations involve reading and surgically updating `living_document.md` using the `write` tool.
