from pathlib import Path
from pypdf import PdfReader


def load_pdf(file_path: str) -> dict:
    """
    Load a PDF file and extract its text.

    Returns:
        {
            "text": "...",
            "source": "filename.pdf"
        }
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got: {path.suffix}")

    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    full_text = "\n\n".join(pages)

    return {
        "text": full_text,
        "source": path.name,
    }