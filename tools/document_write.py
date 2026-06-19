import os


class DocumentWrite:
    """Replace a target string inside a markdown document."""

    def __init__(self, source_file: str):
        self._source_file = source_file

        if not os.path.exists(self._source_file):
            raise FileNotFoundError(f"Source file not found: {self._source_file}")

    def update(self, target: str, value: str):
        """
        Replace first occurrence of `target` string with `value`.
        """

        # Read file
        with open(self._source_file, "r", encoding="utf-8") as f:
            text = f.read()

        # Validate match
        if target not in text:
            raise ValueError(f"Target text not found in document:\n{target}")

        # Replace only first occurrence
        updated_text = text.replace(target, value, 1)

        # Write back
        with open(self._source_file, "w", encoding="utf-8") as f:
            f.write(updated_text)
