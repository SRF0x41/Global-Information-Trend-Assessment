import os


class DocumentWrite:
    """Select certain lines of text to be replaced"""

    def __init__(self, source):
        """
        Store source file internally as object state.
        
        Args:
            source (str): Path to markdown file containing text to find in target
        """
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source file not found: {source}")

        self._source = source  # internal private variable

    def update(self, target, value):
        """
        Replace a block of text in a target markdown file with new content.

        Args:
            target (str): Path to markdown file to modify
            value (str): Replacement text
        """

        # --- Read source file (text to locate in target)
        with open(self._source, "r", encoding="utf-8") as f:
            source_text = f.read().strip()

        # --- Read target file
        if not os.path.exists(target):
            raise FileNotFoundError(f"Target file not found: {target}")

        with open(target, "r", encoding="utf-8") as f:
            target_text = f.read()

        # --- Ensure match exists
        if source_text not in target_text:
            raise ValueError("Source text not found in target file")

        # --- Replace first occurrence only
        updated_text = target_text.replace(source_text, value, 1)

        # --- Write back to target
        with open(target, "w", encoding="utf-8") as f:
            f.write(updated_text)