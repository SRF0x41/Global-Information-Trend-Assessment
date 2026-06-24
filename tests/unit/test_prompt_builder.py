import pytest
import os
from agent_reasoning.prompt_builder import PromptBuilder


def test_prompt_builder_add_text():
    builder = PromptBuilder(max_tokens=100)
    builder.add_text("Hello")
    builder.add_text("World")
    assert builder.get_prompt() == "Hello\n\nWorld"
    assert builder.get_total_tokens() > 0


def test_prompt_builder_add_from_file(tmp_path):
    file = tmp_path / "test_file.txt"
    file.write_text("Hello from file", encoding="utf-8")

    builder = PromptBuilder(max_tokens=100)
    builder.add_from_file(str(file))

    assert "Hello from file" in builder.get_prompt()
    assert builder.get_total_tokens() > 0


def test_prompt_builder_truncation():
    # Use a small max_tokens to force truncation
    builder = PromptBuilder(max_tokens=5)
    builder.add_text("This is a very long string that will be truncated")

    prompt = builder.get_prompt()
    assert len(prompt) <= 50  # It's characters, but tokens are what matters.
    # Actually, tiktoken tokens are different.
    # But it should be significantly shorter.
    assert len(prompt.encode("utf-8")) < 50


def test_prompt_builder_remove_source(tmp_path):
    file1 = tmp_path / "f1.txt"
    file1.write_text("Content 1", encoding="utf-8")
    file2 = tmp_path / "f2.txt"
    file2.write_text("Content 2", encoding="utf-8")

    builder = PromptBuilder(max_tokens=100)
    builder.add_from_file(str(file1))
    builder.add_from_file(str(file2))

    assert "Content 1" in builder.get_prompt()
    assert "Content 2" in builder.get_prompt()

    builder.remove_source(str(file1))

    assert "Content 1" not in builder.get_prompt()
    assert "Content 2" in builder.get_prompt()


def test_prompt_builder_file_not_found():
    builder = PromptBuilder()
    with pytest.raises(FileNotFoundError):
        builder.add_from_file("non_existent_file.txt")
