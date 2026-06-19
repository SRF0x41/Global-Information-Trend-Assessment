import shutil
from datetime import datetime
from pathlib import Path


def main():
    """
    Backs up the current living_document.md to a timestamped file
    and resets living_document.md to its initial template state.
    """
    living_doc_path = Path("living_document.md")

    if not living_doc_path.exists():
        print(f"Error: {living_doc_path} not found.")
        return

    # 1. Create a backup of the current state
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(f"living_document_backup_{timestamp}.md")
    shutil.copy(living_doc_path, backup_path)
    print(f"Successfully backed up current state to: {backup_path}")

    # 2. Define the initial template
    # This matches the initial state of the living_document.md
    initial_template = (
        "### LIVING DOCUMENT\n\n"
        "### Initial Research Priorities\n\n"
        "Rank the most important areas to investigate.\n\n"
        "### Foundational Hypotheses\n\n"
        "Provide tentative hypotheses about the current cultural moment.\n\n"
        "These are not conclusions.\n\n"
        "They are starting assumptions to test.\n\n"
        "### Search Plan\n\n"
        "Generate 25-50 search queries designed to build a broad initial understanding of:\n\n"
        "* psychology\n"
        "* social behavior\n"
        "* culture\n"
        "* identity\n"
        "* meaning\n"
        "* technology's influence on human behavior\n\n"
        "Each query should include a brief explanation of why it is valuable."
    )

    # 3. Reset the living document to the template
    try:
        with open(living_doc_path, "w", encoding="utf-8") as f:
            f.write(initial_template)
        print("Successfully reset living_document.md to the initial template.")
    except Exception as e:
        print(f"Error writing to {living_doc_path}: {e}")


if __name__ == "__main__":
    main()
