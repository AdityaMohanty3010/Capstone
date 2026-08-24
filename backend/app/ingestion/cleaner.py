import re


def clean_text(text: str) -> str:
    """
    Clean extracted document text while preserving its meaning.
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove trailing/leading whitespace from each line
    lines = [line.strip() for line in text.split("\n")]

    # Remove completely empty lines
    lines = [line for line in lines if line]

    # Rebuild the text
    text = "\n".join(lines)

    # Replace multiple spaces with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Limit excessive consecutive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()