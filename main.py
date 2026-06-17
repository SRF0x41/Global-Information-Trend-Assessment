import json
import logging
from llm_clients.lm_studio_client import LmStudioClient
from pathlib import Path
from agent_reasoning.prompt_builder import PromptBuilder

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
        server_response = llm_client.chat_completions(messages=summary_payload)
        content = server_response["choices"][0]["message"]["content"]
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
        server_response = llm_client.chat_completions(messages=planning_payload)
        content = server_response["choices"][0]["message"]["content"]
        print(f"Planning Response:{content}")
        return content
    except Exception as e:
        print(f"Failed Chat Completion: {e}")


def write_document(text, append_prompt: Optional[str] = None):
    write_prompt = PromptBuilder()
    write_prompt.add_text(
        
        """
            Given the following text, make edits to the living document, you are encouraged to make multiple edits.
        
        """
    )
    write_prompt.add_text(text)
    write_prompt.add_text("Here is the living document")
    write_prompt.add_from_file(LIVING_DOCUMENT)
    
    if append_prompt:
        write_prompt.add_text(append_prompt)

    response = llm_client.send(
        system=Path("tools/tool_schema/write_skill.md").read_text(encoding="utf-8"),
        user=write_prompt.get_prompt(),
    )
        
    from parsers.response_parser import ResponseParser
    import json

    parser = ResponseParser()

    tool_calls = parser.extract_tool_calls(response)

    for t in tool_calls:
        print(json.dumps(t, indent=4))
    
    


def main():
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
    planning_schema = planning()
    summarize(planning_schema)
    
    write_document(text=planning_schema)

    """
            Search:
            living document + SEARCH_PROMPT + TOOL_SCHEMA
                - Conduct web searches according to the plan set out in the living document
                - Tools call to search and edit living document, remember all notes are kept in the living documents,
                write notes and analyses directly to the living document.

            Extract:
            living document + EXTRACT_PROMPT + TOOL_SCHEMA
                - Extract relevant 'signals' and edit the living document
                - Tool call to edit the living document

            Compare:
            living document + COMPARE_PROMPT + TOOL_SCHEMA
                - does this change anything in the report

            Refactor:
            living document + REFACTOR_PROMPT + TOOL_SCHEMA
                - Make the report more human readable

            BREAK:
            living document + BREAK_PROMPT
                - Make an assesment to see if the report is ready
    """


if __name__ == "__main__":
    main()
