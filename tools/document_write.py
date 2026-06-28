import os
import re
import difflib


class DocumentWrite:
    """Surgically update a markdown document.

    Two modes:
    - Section-based (primary): target by header name, append or replace content.
    - String-based (fallback): exact/fuzzy match a target string.
    """

    def __init__(self, source_file: str):
        self._source_file = source_file

        if not os.path.exists(self._source_file):
            raise FileNotFoundError(f"Source file not found: {source_file}")

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def apply(self, args: dict):
        """Dispatch to the right update mode based on args keys.

        Accepted arg shapes:
          - {"section": "...", "operation": "append|replace", "content": "..."}
          - {"target": "...", "value": "..."}            # legacy
          - {"value": "..."}                             # legacy append
        """
        if "section" in args:
            return self.update_section(
                section=args["section"],
                operation=args.get("operation", "append"),
                content=args["content"],
            )
        if args.get("operation") == "create":
            return self.create(args["content"])
        # Legacy: target / value
        target = args.get("target")
        value = args.get("value")
        if target is None and value is not None:
            return self.update(target=None, value=value)
        if target is not None:
            return self.update(target=target, value=value or "")
        raise ValueError("apply() needs either 'section' or 'value' in args")

    # -- Create --------------------------------------------------------- #

    def create(self, content: str):
        """Write content as the initial document body."""
        with open(self._source_file, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

    # -- Section-based updates ------------------------------------------ #

    def update_section(self, section: str, operation: str, content: str):
        """Update content under a named section header.

        Parameters
        ----------
        section: markdown header text (e.g. "EMERGING SIGNALS").
            The method searches for a line like `# EMERGING SIGNALS` or
            `## EMERGING SIGNALS` — any heading level.
        operation: "append" | "replace"
            append  — add *content* after the existing section body.
            replace — swap the entire section body with *content*.
        content: new / additional markdown text.
        """
        with open(self._source_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        header_idx = self._find_header_line(lines, section)
        if header_idx is None:
            raise ValueError(
                f"Section header not found: {section}\n"
                f"Available sections: {self.list_sections()}"
            )

        start_of_next = self._find_next_header(lines, header_idx + 1)

        if operation == "replace":
            new_body = self._wrap_content(content)
            lines[header_idx + 1:start_of_next] = [new_body + "\n"]
        elif operation == "append":
            # Insert before the next header, or at end of file
            insert_at = start_of_next if start_of_next is not None else len(lines)
            new_body = self._wrap_content(content)
            lines.insert(insert_at, new_body + "\n")
        else:
            raise ValueError(f"Unknown operation: {operation}")

        with open(self._source_file, "w", encoding="utf-8") as f:
            f.writelines(lines)

    # -- String-based updates (legacy + fuzzy) -------------------------- #

    def update(self, target: str, value: str, fuzzy_threshold: float = 0.85):
        """Replace first occurrence of `target` with `value`.

        If `target` isn't found exactly, falls back to fuzzy matching
        (difflib.SequenceMatcher) when similarity >= fuzzy_threshold.
        If `target` is None/empty, append `value` to end of file.
        """
        with open(self._source_file, "r", encoding="utf-8") as f:
            text = f.read()

        if not target:
            updated_text = text + value
        else:
            if target in text:
                updated_text = text.replace(target, value, 1)
            else:
                # Fuzzy fallback
                matched = self._fuzzy_find(text, target, threshold=fuzzy_threshold)
                if matched is not None:
                    actual_target, _ = matched
                    updated_text = text.replace(actual_target, value, 1)
                else:
                    raise ValueError(
                        f"Target not found in document (no fuzzy match >= {fuzzy_threshold}):\n{target}"
                    )

        with open(self._source_file, "w", encoding="utf-8") as f:
            f.write(updated_text)

    # ------------------------------------------------------------------ #
    # Internals
    # ------------------------------------------------------------------ #

    def list_sections(self) -> list:
        """Return all section header texts in the document."""
        with open(self._source_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        sections = []
        for line in lines:
            m = re.match(r"^#+\s+(.+)$", line.strip())
            if m:
                sections.append(m.group(1).strip())
        return sections

    @staticmethod
    def _find_header_line(lines: list, section: str, fuzzy_threshold: float = 0.85) -> int | None:
        """Find line index of a header matching *section* text.

        Exact match first (case-insensitive). If no exact match, fall back
        to fuzzy matching against all header texts using difflib.
        """
        # Exact match (case-insensitive)
        pattern = re.compile(r"^#+\s+" + re.escape(section) + r"\s*$", re.IGNORECASE)
        for i, line in enumerate(lines):
            if pattern.match(line.rstrip()):
                return i

        # Fuzzy fallback: compare against all header texts
        headers = []
        for i, line in enumerate(lines):
            m = re.match(r"^#+\s+(.+)$", line.strip())
            if m:
                headers.append((i, m.group(1).strip()))

        best_ratio = 0.0
        best_idx = None
        for idx, text in headers:
            ratio = difflib.SequenceMatcher(None, section, text).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_idx = idx

        if best_ratio >= fuzzy_threshold:
            return best_idx
        return None

    @staticmethod
    def _find_next_header(lines: list, start: int) -> int | None:
        """Find the next markdown header at or after *start*."""
        for i in range(start, len(lines)):
            if re.match(r"^#+\s+", lines[i].strip()):
                return i
        return None  # end of file

    @staticmethod
    def _find_separator(lines: list, start: int, end_limit: int | None) -> int | None:
        """Find a `---` separator line in [start, end_limit)."""
        limit = end_limit if end_limit is not None else len(lines)
        for i in range(start, limit):
            if lines[i].strip() == "---":
                return i
        return None

    @staticmethod
    def _wrap_content(content: str) -> str:
        """Ensure content has a leading/trailing blank line for clean markdown."""
        if not content.strip():
            return ""
        text = content.strip()
        return "\n" + text + "\n"

    @staticmethod
    def _fuzzy_find(text: str, target: str, threshold: float = 0.85):
        """Try to find *target* in *text* by fuzzy-matching paragraphs.

        Splits text into chunks (paragraphs / lines) and returns the best
        (matched_chunk, ratio) if ratio >= threshold, else None.
        """
        paragraphs = text.split("\n\n")
        best_match = None
        best_ratio = 0.0

        for para in paragraphs:
            ratio = difflib.SequenceMatcher(None, target, para).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = para

        if best_ratio >= threshold:
            return (best_match, best_ratio)
        # Also try line-by-line for short targets
        for line in text.splitlines():
            ratio = difflib.SequenceMatcher(None, target.strip(), line.strip()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = line

        if best_ratio >= threshold:
            return (best_match, best_ratio)
        return None
