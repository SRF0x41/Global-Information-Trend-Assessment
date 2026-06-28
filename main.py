import json
import logging
import time
from llm_clients.lm_studio_client import LmStudioClient
from pathlib import Path
from agent_reasoning.prompt_builder import PromptBuilder
from parsers.response_parser import ResponseParser
from typing import List, Dict, Any, Optional
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

""" Shared classes """
llm_client = LmStudioClient()

""" Shared variables """
SYSTEM_PROMPT = Path("prompts/SYSTEM_PROMPT.md")
PLAN_PROMPT = Path("prompts/PLAN_PROMPT.md")
LIVING_DOCUMENT = Path("living_document.md")
WRITE_TO_LIVING_DOCUMENT = Path("WRITE_TO_LIVING_DOCUMENT.md")

ZEITGEIST_REPORT = Path("zeitgeist_report.md")


# md_content = Path("report.md").read_text(encoding="utf-8")


def summarize(text):
    # general purpose summary of the given text, mostly used to print what the llm produced
    summary_payload = [
        {
            "role": "system",
            "content": "Summarize the following text in one paragraph, be consise.",
        },
        {"role": "user", "content": text},
    ]
    try:
        content = llm_client.send_streaming(
            user=summary_payload[1]["content"],
            system=summary_payload[0]["content"],
        )
        print(content)
    except Exception as e:
        print(f"Failed Chat Completion: {e}")


def planning():
    print("--- PLANNING ---")
    planning_payload = [
        {"role": "system", "content": SYSTEM_PROMPT.read_text(encoding="utf-8")},
        {"role": "user", "content": PLAN_PROMPT.read_text(encoding="utf-8")},
        {"role": "user", "content": LIVING_DOCUMENT.read_text(encoding="utf-8")},
    ]
    try:
        content = llm_client.send_streaming(
            system=planning_payload[0]["content"],
            user=planning_payload[1]["content"] + "\n\n" + planning_payload[2]["content"],
        )
        print(f"Planning Response:{content}")
        return content
    except Exception as e:
        print(f"Failed Chat Completion: {e}")


def write_document_test(text, append_prompt: Optional[str] = None):
    write_prompt = PromptBuilder()
    write_prompt.add_text(
        """You are about to receive two things:
        1. Notes extracted from source material.
        2. The current Living Document.

        Your job is to update the Living Document so that it incorporates the insights found in the notes."""
        )
    write_prompt.add_text("""
        ## NOTES
        """)
    write_prompt.add_text(text)
    write_prompt.add_text("""
        ## INSTRUCTION
        Read the notes carefully. Then update the Living Document however you see fit.

        You have complete freedom over how you write:
        - Write wherever you want — Working Notes, structured sections, or both
        - Append new content, edit existing passages, or rewrite sections entirely
        - Write in whatever voice and style you find most useful — analytical, narrative, speculative, critical
        - Draw your own conclusions. Make connections the notes don't explicitly state. If something strikes you as significant, write about it.
        - You can disagree with the existing document and revise it. If new evidence changes your mind, say so.
        - You are not bound to process every note mechanically. Write what matters, in the way that matters most.

        The Living Document is your working memory — treat it like a notebook you're actively thinking in, not a form you're filling out.

        Below is the current Living Document.""")
    write_prompt.add_from_file(LIVING_DOCUMENT)
    write_prompt.add_text(
        "Below is the tool schema that shows you how to call `write`."
    )
    write_prompt.add_from_file(Path("tools/tool_schema/write_skill.md"))

    if append_prompt:
        write_prompt.add_text(append_prompt)

    response = llm_client.send_streaming(
        system=SYSTEM_PROMPT.read_text(encoding="utf-8"),
        user=write_prompt.get_prompt(),
    )

    print(response)

    parser = ResponseParser()

    tool_calls = parser.extract_tool_calls(response)
    from tools.document_write import DocumentWrite

    writer = DocumentWrite(LIVING_DOCUMENT)

    print("writing")
    print(80 * "=")

    for t in tool_calls:
        print(json.dumps(t.get_raw_json(), indent=4))
        args = t.get_tool_arguments()
        try:
            writer.apply(args)
        except Exception as e:
            print(f"Error applying write: {e}")


def search_store_analyze(query):
    from tools.serper_search import SerperSearch

    serper = SerperSearch()

    # Step1: Generate a list of search results from the first page on Google
    first_page_articles = serper.search(query)

    # Step2: Read and parse every article in the first page results
    from tools.text_extractor import TextExtractor

    page_parser = TextExtractor()

    # Step3: Initialize database for storing results
    try:
        from database.search_database import SearchDatabase

        db = SearchDatabase()
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")
        db = None

    # Step4: Process each article and store in database
    for r in first_page_articles:
        pulled_text = page_parser.extract_text(r.get("url"))
        title = r.get("title", "No Title")

        # Skip pages that returned HTTP 4xx/5xx or fetch errors
        if pulled_text.startswith("[SKIPPED") or pulled_text.startswith("[ERROR"):
            print(f"\n[SKIPPED] {title} — {pulled_text}")
            continue

        print(f"\n[Article Found]")
        print(f"Query: {query}")
        print(f"Title: {title}")
        print(f"Snippet: {pulled_text[:200].replace('\n', ' ')}...")
        print("-" * 30)

        # Store the result in the database if database is available
        if db:
            try:
                # Store the result in the database
                title = r.get("title", "")
                url = r.get("url", "")

                # Attempt to extract date posted from Serper results if available
                date_posted = r.get("date", None)

                db.store_result(
                    url=url,
                    title=title,
                    content=pulled_text,
                    search_query=query,
                    date_posted=date_posted,
                )
            except Exception as e:
                print(f"Warning: Could not store result in database: {e}")
        else:
            print("Database not available, skipping storage")

        # Step 5: have the llm take the entire article and gather evidence

        analyze_prompt = PromptBuilder()
        analyze_prompt.add_from_file(SYSTEM_PROMPT)
        
        ### Repeating work here

        EXTRACT_PROMPT = Path("prompts/EXTRACT_PROMPT.md")
        analyze_prompt.add_from_file(EXTRACT_PROMPT)
        analyze_prompt.add_text("Here is the living document.")
        analyze_prompt.add_from_file(LIVING_DOCUMENT)
        analyze_prompt.add_text("Here is the following article to analyze.")
        analyze_prompt.add_text(pulled_text)

        response = llm_client.send_streaming(
            user=analyze_prompt.get_prompt()
        )
        print("Analyse Response")
        print(response)
        write_document_test(response)


def database_search(query: str, limit: int = 1) -> List[Dict[str, Any]]:
    """
    Search the database for relevant results based on a query.
    Returns one or more relevant results (not exact matches).
    """
    try:
        from database.search_database import SearchDatabase

        db = SearchDatabase()

        # Perform flexible search using the database's search capability
        results = db.search(query, limit=limit)

        return results

    except Exception as e:
        print(f"Error performing database search: {e}")
        return []

        # Step 5:


def generate_search_queries(max_retries=3):
    for attempt in range(max_retries):
        # Step 1: Generate search queries based on the current living document state
        SEARCH_PROMPT = Path("prompts/SEARCH_PROMPT.md")
        search_prompt = PromptBuilder()
        search_prompt.add_from_file(SYSTEM_PROMPT)
        search_prompt.add_from_file(SEARCH_PROMPT)
        search_prompt.add_text(
            """You are about to receive the current state of the Living Document.

        Your job is to produce a comprehensive list of web searches that will reduce uncertainty, test contradictions, and expand weak signals found in the document."""
                )
        search_prompt.add_text("Below is the current Living Document.")
        search_prompt.add_from_file(LIVING_DOCUMENT)
        search_prompt.add_text(
            """
            ## INSTRUCTION
            Read the Living Document carefully. For every uncertainty, contradiction, weak signal, blind spot, or open research question it contains, call the `web_search` tool to investigate it.

            - Call `web_search` as many times as needed to cover the document's open areas.
            - Each call must target a different question or angle. Do NOT repeat the same query.
            - Phrase queries to uncover behavioral patterns, psychological shifts, and cultural trends, not just headlines.
            - Make one `web_search` tool call per line. Do NOT wrap them in code blocks or add explanations between calls."""
                    )
        SEARCH_TOOL_CARD = Path("tools/tool_schema/web_searcher_skill.md")
        search_prompt.add_text("Use the following tool card to call web_search:")
        search_prompt.add_from_file(SEARCH_TOOL_CARD)

        # Generate search queries using LLM
        response = llm_client.send_streaming(
            user=search_prompt.get_prompt()
        )
        print(f"Raw search tool calls {response}")
        print(response)

        # Parse the tool calls from the LLM response
        parser = ResponseParser()
        tool_calls = parser.extract_tool_calls(response)

        # Debug: print the raw LLM response
        print(f"LLM Response for search queries (attempt {attempt + 1}):")
        print(response)

        # Return list of queries instead of executing them
        queries = []
        print("Verifying that each tool call is unique")
        for t in tool_calls:
            print(t)
            # Extract the search query from the tool call
            query = t.get_tool_arguments().get("query")
            if query:
                queries.append(query)

        if queries:
            return queries

        print(f"No queries generated on attempt {attempt + 1}. Retrying...")

    print("Failed to generate search queries after maximum retries.")
    return []

def generate_refactor():
    """
    Refactor:
    current zeitgeist report + REFACTOR_PROMPT + SYSTEM_PROMPT
        - The LLM reads the existing report and outputs a refined, improved version
        - Response is written directly to zeitgeist_report.md (full rewrite each pass)
    """
    print("--- REFACTOR: Generating Zeitgeist Report ---")

    REFACTOR_PROMPT = Path("prompts/REFACTOR_PROMPT.md")

    # Build prompt: system + refactor instructions + current report
    refactor = PromptBuilder()
    refactor.add_from_file(REFACTOR_PROMPT)

    if ZEITGEIST_REPORT.exists() and ZEITGEIST_REPORT.stat().st_size > 0:
        refactor.add_text("Below is the current Zeitgeist Report — refine it.")
        refactor.add_from_file(ZEITGEIST_REPORT)
    else:
        refactor.add_text(
            "No existing Zeitgeist Report found. Produce one from scratch."
        )

    refactor.add_text(
        "\nProduce the complete, refined Zeitgeist Report essay as your response."
    )

    response = llm_client.send_streaming(
        system=SYSTEM_PROMPT.read_text(encoding="utf-8"),
        user=refactor.get_prompt(),
    )

    if not response:
        print("Failed to generate Zeitgeist Report — LLM returned empty response.")
        return None

    # Write the LLM response directly to the zeitgeist report file
    ZEITGEIST_REPORT.write_text(response, encoding="utf-8")
    print(f"\nZeitgeist Report written to {ZEITGEIST_REPORT}")
    summarize(response)
    return response


def generate_synthesize():
    """
    Synthesize:
    living document + SYNTHESIZE_PROMPT + SYSTEM_PROMPT + WRITE_TOOL_SCHEMA
        - The LLM reads the Living Document and identifies clusters of signals
          that have enough density to coalesce into cohesive prose.
        - Makes multiple surgical `write` tool calls — one per section.
        - Does NOT rewrite the entire document. Only touches sections ready for it.
        - Freely deletes stale, redundant, or irrelevant information.
    """
    print("--- SYNTHESIZE: Coalescing Living Document ---")

    SYNTHESIZE_PROMPT = Path("prompts/SYNTHESIZE_PROMPT.md")

    synthesize_prompt = PromptBuilder()
    synthesize_prompt.add_from_file(SYNTHESIZE_PROMPT)
    synthesize_prompt.add_text("Below is the current Living Document.")
    synthesize_prompt.add_from_file(LIVING_DOCUMENT)
    synthesize_prompt.add_text(
        "\nBelow is the tool schema that shows you how to call `write`."
    )
    synthesize_prompt.add_from_file(Path("tools/tool_schema/write_skill.md"))

    response = llm_client.send_streaming(
        system=SYSTEM_PROMPT.read_text(encoding="utf-8"),
        user=synthesize_prompt.get_prompt(),
    )

    if not response:
        print("Failed to synthesize — LLM returned empty response.")
        return None

    parser = ResponseParser()
    print(response)
    tool_calls = parser.extract_tool_calls(response)

    from tools.document_write import DocumentWrite
    writer = DocumentWrite(LIVING_DOCUMENT)

    print("Applying surgical edits")
    print(80 * "=")

    for t in tool_calls:
        print(json.dumps(t.get_raw_json(), indent=4))
        args = t.get_tool_arguments()
        try:
            writer.apply(args)
        except Exception as e:
            print(f"Error applying write: {e}")

    summarize(response)
    return response



def main():
    start_time = time.time()
    """
    Preliminary flow of the program


        PUT THE SYSTEM PROMPT EVERY TIME "role" : "system" BECAUSE LM STUDIO IS STATELESS

        Agent loop:
            Planning:
            living document + SYSTEM_PROMPT + PLAN_PROMPT
                - Tool call to edit the living document
                - insert planing steps, no edits

            (Consider parsing the living document into parts and processing each part as a unit?
            But it may be usefull to have the entire document visible. Perhaps quantize the document for
            very manual work such as searching, )
            
            
    """
    
    
    for i in range(4):
        planning_schema = planning()
        summarize(planning_schema)

        write_document_test(text=planning_schema)

        """
                Search:
                living document + SEARCH_PROMPT + TOOL_SCHEMA
                    - Conduct web searches according to the plan set out in the living document
                    - Tools call to search and edit living document, remember all notes are kept in the living documents,
                    write notes and analyses directly to the living document.            
        """
        # Ask the llm to create a list of search queries
        search_queries = generate_search_queries()
        print(f"Search queries produced: {len(search_queries)}")
        
        """
                Extract:
                living document + EXTRACT_PROMPT + TOOL_SCHEMA
                    - Extract relevant 'signals' and edit the living document
                    - Tool call to edit the living document
        """
        for s in search_queries:
            print(f"Query: {s}")
            search_store_analyze(s)
            generate_synthesize()


        """

                Compare: (Were ignoring this step for now, i forgot what i meant and doesnt seem relevant at the moment,
                i think this is for when the doc needs to be ammended with new info, i think extract is already doing this)
                living document + COMPARE_PROMPT + TOOL_SCHEMA
                    - does this change anything in the report
        """
        
        """

                Refactor:
                living document + REFACTOR_PROMPT + TOOL_SCHEMA
                    - Make the report more human readable
                    
        """
            
        generate_refactor()

    elapsed = time.time() - start_time
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"\n{80 * '='}")
    print(f"Complete. Total time: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")

    """

            BREAK:
            living document + BREAK_PROMPT
                - Make an assesment to see if the report is ready
    """


if __name__ == "__main__":
    main()
    # import subprocess
    # import sys
    # subprocess.run([sys.executable, "reset_living_doc.py"])
