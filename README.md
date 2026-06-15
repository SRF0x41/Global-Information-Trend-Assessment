# Zeitgeist Intelligence System (ZIS)

An autonomous, agentic research framework designed to monitor, synthesize, and model the evolving global zeitgeist. Rather than merely summarizing news, the system identifies patterns, narratives, and tensions across multiple domains (cultural, technological, economic, political, social, and psychological).

## Core Concept: The Living Document

At the heart of the system is the **Living Document** (`living_document.md`). This is the agent's primary working memory and state. The agent iteratively interacts with this document to:

1.  **Plan** research trajectories based on the current state.
2.  **Search** for relevant signals via web search tools.
3.  **Extract** meaningful patterns and signals (not just summaries).
4.  **Compare** new data against existing models in the document.
5.  **Refactor** the document to improve coherence and clarity.
6.  **Assess** when the current understanding is sufficient or if the research loop should break.

## Agentic Workflow

The system operates through a continuous, iterative loop of specialized tasks:

*   **Planning:** Formulates research strategies and identifies information gaps.
*   **Search:** Executes targeted searches to gather external signals.
*   **Extraction:** Processes information to identify "signals"—patterns, themes, or tensions—rather than mere summaries.
*   **Comparison:** Evaluates new signals to see if they support, weaken, or contradict existing narratives.
*   **Refactoring:** Continuously refines the living document, evolving from a collection of facts into a coherent model of reality.
*   **Assessment:** Determines if the current model is robust or requires further investigation.

## Analytical Framework

The system evaluates signals across several key domains to build a multidimensional model:
- **Cultural:** Changes in values, identity, art, media, and behavior.
- **Technological:** New technologies, adoption patterns, and societal reactions.
- **Economic:** Consumer behavior, labor trends, and market sentiment.
- **Political:** Governance, ideology, and geopolitical shifts.
- **Social:** Demographics, relationships, and collective behavior.
- **Psychological:** Fear, optimism, aspirations, and emotional tone.

## Project Structure

```
.
├── main.py             # Entry point for the agentic loop
├── living_document.md  # The central, evolving state of the system
├── prompts/            # Specialized instructional prompts for each agentic step
├── tools/              # Agent capabilities (web search, document writing, etc.)
├── requirements.txt    # System dependencies
└── seed_prompt.md      # Core directive and analytical framework for the agent
```

## Getting Started

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

### Usage
The system is designed to be driven by an LLM-based agent (such as Claude) that can execute the defined tools and prompts.
