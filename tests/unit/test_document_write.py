import pytest
import os
from tools.document_write import DocumentWrite

@pytest.fixture
def temp_doc(tmp_path):
    doc_path = tmp_path / "living_document.md"
    doc_path.write_text("# Living Document\n\nCurrent State: Initial", encoding="utf-8")
    return str(doc_path)

def test_document_update_success(temp_doc):
    dw = DocumentWrite(temp_doc)
    dw.update("Current State: Initial", "Current State: Updated")

    with open(temp_doc, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Current State: Updated" in content
    assert "Current State: Initial" not in content

def test_document_update_not_found(temp_doc):
    dw = DocumentWrite(temp_doc)
    with pytest.raises(ValueError, match="Target text not found"):
        dw.update("Non-existent text", "Replacement")

def test_document_init_no_file():
    with pytest.raises(FileNotFoundError):
        DocumentWrite("non_existent_file.md")

def test_document_update_first_occurrence_only(tmp_path):
    doc_path = tmp_path / "repeat.md"
    doc_path.write_text("A - B - A", encoding="utf-8")

    dw = DocumentWrite(str(doc_path))
    dw.update("A", "C")

    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == "C - B - A"
