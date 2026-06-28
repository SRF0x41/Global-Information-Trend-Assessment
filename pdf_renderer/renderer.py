"""Render a markdown file to PDF."""

from pathlib import Path
from weasyprint import HTML
import markdown


class PdfRenderer:
    """Convert a .md file to a .pdf file."""

    DEFAULT_CSS = """
        @page {
            size: A4;
            margin: 2.5cm 2cm;
        }
        body {
            font-family: Georgia, serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
        }
        h1 {
            font-size: 24pt;
            margin-top: 1em;
            font-weight: bold;
        }
        h2 {
            font-size: 18pt;
            margin-top: 1.2em;
            border-bottom: 1px solid #ccc;
            padding-bottom: 0.2em;
        }
        h3 {
            font-size: 14pt;
            margin-top: 1em;
        }
        p {
            margin: 0.6em 0;
        }
        blockquote {
            margin: 1em 0;
            padding: 0.5em 1em;
            border-left: 3px solid #ccc;
            color: #555;
            font-style: italic;
        }
        code {
            font-family: "Courier New", monospace;
            background: #f4f4f4;
            padding: 0.1em 0.3em;
            font-size: 0.9em;
        }
        pre {
            background: #f4f4f4;
            padding: 0.8em;
            border-radius: 3px;
            overflow-x: auto;
        }
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 1.5em 0;
        }
    """

    def __init__(self, css: str = None):
        self.css = css or self.DEFAULT_CSS

    def render(self, md_path: str, pdf_path: str = None) -> Path:
        """Read a markdown file and write a PDF. Returns the output path."""
        path = Path(md_path)
        if not path.exists():
            raise FileNotFoundError(f"Markdown file not found: {md_path}")

        md_text = path.read_text(encoding="utf-8")
        html_body = markdown.markdown(md_text, extensions=["extra", "nl2br"])

        html_full = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{self.css}</style></head>
<body>{html_body}</body></html>"""

        out = Path(pdf_path) if pdf_path else path.with_suffix(".pdf")
        HTML(string=html_full).write_pdf(str(out))
        return out
