from dataclasses import dataclass


@dataclass
class ExtractedDocument:
    source_path: str
    text: str


def extract_text(source_path: str) -> ExtractedDocument:
    """Placeholder extraction entry point for PDF, DOCX, MD, and TXT."""
    return ExtractedDocument(source_path=source_path, text="")
