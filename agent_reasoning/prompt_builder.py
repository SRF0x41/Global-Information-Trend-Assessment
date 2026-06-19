import os


class PromptBuilder:
    def __init__(self):
        self.__components = []
        self.__sources = []

    def add_from_file(self, file_path):
        """Appends the contents of a markdown file to the master prompt."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            self.__components.append(content)
            self.__sources.append(file_path)

    def add_text(self, text):
        """Manually append a string to the master prompt."""
        self.__components.append(text)
        self.__sources.append(text)

    def print_sources(self):
        """Print all the sources."""
        print(self.__sources)

    def remove_source(self, source):
        """Remove a source and rebuild the master prompt components."""
        if source in self.__sources:
            index = self.__sources.index(source)
            self.__sources.pop(index)
            self.__components.pop(index)
        else:
            print(f"Source '{source}' not found.")

    def get_prompt(self):
        """Return the combined master prompt as a single string."""
        return "\n\n".join(self.__components)
