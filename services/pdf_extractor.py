from pathlib import Path

import fitz


def extract_pdf_text(file_path: str | Path) -> str:
    """Extract selectable text from every page of a PDF."""
    document = fitz.open(file_path)
    try:
        text = "\n".join(page.get_text() for page in document).strip()
    finally:
        document.close()

    if not text:
        raise ValueError(
            "This PDF has no selectable text. Try a text-based PDF or use manual entry."
        )
    return text
