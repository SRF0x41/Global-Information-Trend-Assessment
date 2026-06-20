import pytest
import os
from tools.document_write import DocumentWrite

def test_document_write_update_success(tmp_path):
    # Create a temporary file
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test_doc.md"
    p.write_text("This is the original text. This is the target.", encoding="utf-8")

    dw = DocumentWrite(str(p))
    dw.update("the target", "the updated value")

    assert p.read_text(encoding="utf-8") == "This is the original text. This is the updated value."

def test_document_write_no_match(tmp_path):
    p = tmp_path / "test_doc.md"
    p.write_text("Original text", encoding="utf-8")

    dw = DocumentWrite(str(p))
    with pytest.raises(ValueError) as excinfo:
        dw.update("non-existent", "value")
    assert "Target text not found" in str(excinfo.value)

def test_document_write_file_not_found():
    with pytest.raises(FileNotFoundError):
        DocumentWrite("non_existent_file.md")

def test_document_write_first_occurrence_only(tmp_path):
    p = tmp_path / "test_doc.md"
    p.write_text("Target. Another target.", encoding="utf-8")

    dw = DocumentWrite(str(p))
    dw.update("Target", "First")

    assert p.read_text(encoding="utf-8") == "First. Another target."
