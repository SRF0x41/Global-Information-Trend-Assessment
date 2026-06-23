# Global Information Trend Assessment

Global Information Trend Assessment is an autonomous, agentic research framework designed to monitor, synthesize, and model the evolving global zeitgeist. Rather than merely summarizing news, the system identifies patterns, narratives, and tensions across multiple domains (Cultural, Technological, Economic, Political, Social, and Psychological) to build a multidimensional model of the current moment.

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
6.  **Assessment:** Determines if the current model is robust or requires further investigation.

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

The system is built using a modular architecture designed for extensible agentic research:

*   **`main.py`**: The central orchestrator of the agentic loop.
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

## Key Components

### Prompts
The system uses specialized prompt files for each step of the workflow:
- `PLAN_PROMPT.md`: For planning the research strategy
- `SEARCH_PROMPT.md`: For conducting web searches
- `EXTRACT_PROMPT.md`: For extracting signals from content
- `COMPARE_PROMPT.md`: For comparing new information with existing knowledge
- `REFINE_PROMPT.md`: For refining and improving the living document
- `ASSESSMENT_PROMPT.md`: For assessing the robustness of the current model

### Tools
The system includes several core tools:
- **Web Searcher**: Performs web searches using DuckDuckGo and extracts content from results
- **Document Writer**: Updates the living document with new information

## Development Guide

This project is designed to be an autonomous research agent that continuously evolves its understanding of the current zeitgeist. The development approach emphasizes:

1. **Modular Prompt Engineering**: Each step of the workflow has a dedicated prompt file for precise control over agent behavior
2. **Living Document Architecture**: The system maintains a persistent, evolving knowledge base that guides future research
3. **Cross-Domain Analysis**: Integration of psychological, social, and cultural insights to avoid shallow news analysis

### Core Development Patterns

- **Prompt Separation**: Each stage has its own specialized prompt to ensure precise agent behavior
- **State Persistence**: The `living_document.md` maintains all state between iterations
- **Iterative Refinement**: The system continuously improves its understanding through feedback loops
- **Domain Integration**: All analysis considers the six key domains to avoid narrow perspectives

## Roadmap

*   **Primary Source Analysis:** Focus on analyzing primary sources (e.g., trending songs, social media posts, popular media) to better understand underlying cultural sentiment and messaging (try to differentiate between organic popularity and private interest popularity).
*   **Expanded Domain Support:** Further integrate more granular data points into the six key dimensions.
*   **Automated Assessment Loops:** Refine the assessment step to trigger deeper, autonomous investigations into conflicting signals.
*   **Enhanced Tool Integration:** Expand tool capabilities to include more diverse data sources and analysis methods.

## Contributing

This is an experimental research framework. Contributions are welcome in the form of:

- Improvements to prompt engineering
- Expansion of analytical frameworks
- Enhancements to search strategies
- Development of new tools for analysis
