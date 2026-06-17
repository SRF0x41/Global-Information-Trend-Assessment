# Zeitgeist Intelligence System (ZIS)

Zeitgeist Intelligence System (ZIS) is an autonomous, agentic research framework designed to monitor, synthesize, and model the evolving global zeitgeist. Rather than merely summarizing news, the system identifies patterns, narratives, and tensions across multiple domains (Cultural, Technological, Economic, Political, Social, and Psychological) to build a multidimensional model of the current moment.

## Core Concept: The Living Document

At the heart of the system is the **Living Document** (`living_document.md`). This document serves as the agent's persistent, evolving working memory and state. 

The agent's goal is not to collect a list of news articles, but to **synthesize** information into a coherent, evolving model of reality. It moves from a collection of disconnected facts to a structured understanding of the "zeitgeist."

## Agentic Workflow

The system operates through a continuous, iterative loop of specialized agentic tasks:

1.  **Planning:** Formulates research strategies and identifies information gaps based on the current state of the `living_document.md`.
2.  **Search:** Executes targeted web searches to gather external signals.
3.  **Extraction:** Processes information to identify "signals"—patterns, themes, or tensions—rather than mere summaries.
4.  **Comparison:** Evaluates new signals to see if they support, weaken, or contradict existing narratives in the document.
5.  **Refactoring:** Continuously refines the `living_document.md` to improve human readability, coherence, and depth of understanding.
6.  **Assessment (Break):** Determines if the current model is robust or requires further investigation.

## Analytical Framework

The system evaluates signals across six key dimensions to ensure a holistic perspective:

| Domain | Focus Areas |
| :--- | :--- |
| **Cultural** | Changes in values, identity, art, media, behavior, and cultural norms. |
| **Technological** | New technologies, adoption patterns, societal reactions, and technological displacement. |
| **Economic** | Consumer behavior, labor trends, market sentiment, and wealth distribution. |
| **Political** | Governance, regulation, ideology, geopolitical shifts, and institutional trust. |
| **Social** | Demographics, relationships, community formation, and collective behavior. |
| **Psychological** | Fear, optimism, anxiety, aspirations, and the prevailing emotional tone. |

## Reporting Structure

The final synthesis produced by the system follows a structured format to ensure clarity and depth:

*   **Executive Summary:** A concise description of the current zeitgeist.
*   **Dominant Narratives:** The strongest recurring themes shaping society.
*   **Emerging Narratives:** Patterns that appear significant but are not yet dominant.
*   **Contradictions and Tensions:** Conflicting forces shaping the current moment.
*   **Emotional Climate:** The prevailing emotional and psychological atmosphere.
*   **Weak Signals:** Small developments that may become important in the future.
*   **Evidence Base:** Representative observations supporting the major conclusions.
*   **Open Questions:** Areas where confidence remains low and further investigation is required.

## System Architecture

The system is built using a modular architecture:

*   **`main.py`**: The central orchestrator of the agentic loop.
*   **`agent_reasoning/`**: Logic for constructing and managing complex agentic prompts.
*   **`llm_clients/`**: Interfaces for interacting with Large Language Models (e.g., LM Studio, Anthropic API).
*   **`parsers/`**: Utilities for parsing and processing various data formats, including tool calls.
*   **`prompts/`**: A collection of specialized instructional prompts for each step of the workflow.
*   **`tools/`**: The agent's capabilities, including web searching and document editing.
*   **`living_document.md`**: The evolving state and primary memory of the system.

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
The system is designed to be driven by an LLM-based agent. It can be configured to work with local LLM providers (like LM Studio) for privacy and local development, or via the Anthropic API.

Run the agentic loop:
```bash
python main.py
```
