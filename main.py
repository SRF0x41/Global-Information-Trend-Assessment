import json


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
    pass


if __name__ == "__main__":
    main()
