from ingestion.service import extract_text


def test_extract_text_smoke() -> None:
    doc = extract_text("sample.txt")
    assert doc.source_path == "sample.txt"
