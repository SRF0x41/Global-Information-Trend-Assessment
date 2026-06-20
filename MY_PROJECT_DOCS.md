# Global Information Trend Assessment - Project Documentation

## Overview
This is an autonomous, agentic research framework designed to monitor, synthesize, and model the evolving global zeitgeist. Rather than merely summarizing news, the system identifies patterns, narratives, and tensions across multiple domains (Cultural, Technological, Economic, Political, Social, and Psychological) to build a multidimensional model of the current moment.

## Core Concept: The Living Document
The system centers around a "Living Document" (`living_document.md`) which acts as the agent's persistent, evolving working memory and state. The agent's goal is to synthesize information into a coherent, evolving model of reality, moving from disconnected facts to structured understanding of the "zeitgeist."

## Architecture & Workflow
The system operates through a continuous, iterative loop of specialized agentic tasks:

1. **Planning**: Formulates research strategies and identifies information gaps based on the current state of the `living_document.md`.
2. **Search**: Executes targeted web searches to gather external signals.
3. **Extraction**: Processes information to identify "signals"—patterns, themes, or tensions—rather than mere summaries.
4. **Comparison**: Evaluates new signals to see if they support, weaken, or contradict existing narratives in the document.
5. **Refactoring**: Continuously refines the `living_document.md` to improve human readability, coherence, and depth of understanding.
6. **Assessment**: Determines if the current model is robust or requires further investigation.

## Key Components

### Main Files
- `main.py`: The entry point for the agentic loop (currently a skeleton with planning functionality implemented)
- `living_document.md`: The central, evolving state of the system and primary working memory
- `prompts/`: Contains specialized instructional prompts for each step of the agentic loop
- `tools/`: Contains the agent's capabilities (web_searcher.py, document_write.py)

### Prompts Directory
The system uses specialized prompt files:
- `PLAN_PROMPT.md`: For planning the research strategy  
- `SEARCH_PROMPT.md`: For conducting web searches (currently empty)
- `EXTRACT_PROMPT.md`: For extracting signals from content (currently empty)
- `COMPARE_PROMPT.md`: For comparing new information with existing knowledge (currently empty)
- `REFINE_PROMPT.md`: For refining and improving the living document (currently empty)
- `ASSESSMENT_PROMPT.md`: For assessing the robustness of the current model (currently empty)
- `SYSTEM_PROMPT.md`: The main system prompt defining the agent's role and behavior

### Tools Directory
- `web_searcher.py`: Performs web searches using DuckDuckGo and extracts content from results
- `document_write.py`: Updates the living document with new information

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
The final synthesis produced by the system follows a structured format:
- Executive Summary: A concise description of the current zeitgeist
- Dominant Narratives: The strongest recurring themes shaping society
- Emerging Narratives: Patterns that appear significant but are not yet dominant
- Contradictions and Tensions: Conflicting forces shaping the current moment
- Emotional Climate: The prevailing emotional and psychological atmosphere
- Weak Signals: Small developments that may become important in the future
- Evidence Base: Representative observations supporting major conclusions
- Open Questions: Areas where confidence remains low and further investigation is required

## System Requirements
- Python 3.10+
- Dependencies listed in requirements.txt

## Development Approach
The system is designed to be driven by an LLM-based agent. It can be configured to work with local LLM providers (like LM Studio) for privacy and local development, or via the Anthropic API.

## Current Status
The planning functionality appears to be implemented in main.py, but the other workflow steps (search, extract, compare, refine, assess) are not yet fully developed. The system has a skeleton structure with all necessary components but requires implementation of the full agentic loop.