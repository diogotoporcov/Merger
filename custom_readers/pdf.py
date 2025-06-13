from pathlib import Path

import pymupdf


def is_pdf_file(file_path: Path) -> bool:
    """
    Checks whether the given file is a valid PDF file by attempting to read its first page.

    Args:
        file_path (Path): Path to the file.

    Returns:
        bool: True if the file is a readable PDF, False otherwise.
    """
    try:
        with pymupdf.open(file_path) as doc:
            _ = doc[0]
        return True

    except Exception:
        return False


def extract_pdf_text(file_path: Path) -> str:
    """
    Extracts and concatenates text from all pages of a PDF file.

    Args:
        file_path (Path): Path to the PDF file.

    Returns:
        str: A single string containing all extracted text, with newlines cleaned.
    """
    texts = []
    with pymupdf.open(file_path) as doc:
        for page in doc:
            text = page.get_text()
            if text:
                text = text.replace("\n\n", "")
                texts.append(text)

    full_text = " ".join(texts)
    return full_text
