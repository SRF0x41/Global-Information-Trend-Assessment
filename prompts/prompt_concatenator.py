import os
from markdown import markdown

class PromptConcatenator:
    def __init__(self, prompt_dir='prompts/'):
        self.prompt_dir = prompt_dir
        self.prompts = []

    def add_prompt(self, filename):
        """
        Add a markdown file to the concatenation queue

        Args:
            filename: Name of the markdown file (without path)
        """
        file_path = os.path.join(self.prompt_dir, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        with open(file_path, 'r') as f:
            content = f.read()

        # Convert markdown to HTML (optional - can remove if not needed)
        html_content = markdown(content)

        self.prompts.append((filename, content, html_content))

    def get_concatenated_prompts(self):
        """
        Return all prompts as a single string
        """
        return '\n\n---\n\n'.join([p[1] for p in self.prompts])

    def get_html_prompts(self):
        """
        Return all prompts as HTML-formatted string
        """
        return '\n\n'.join([p[2] for p in self.prompts])

    def list_prompt_files(self):
        """
        Return list of available prompt files
        """
        return [f for f in os.listdir(self.prompt_dir) if f.endswith('.md')]