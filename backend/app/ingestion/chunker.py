import re
from pathlib import Path


def split_into_articles(text: str) -> list[dict]:
    """
    Split a cleaned knowledge-base document into individual articles.

    Expected article format:
        KB-001 — Article title
    """

    pattern = r"(?m)^(KB-\d+)\s+[—-]\s+(.+)$"

    matches = list(re.finditer(pattern, text))

    if not matches:
        return [
            {
                "article_id": "UNKNOWN",
                "title": "Unknown",
                "text": text.strip(),
            }
        ]

    articles = []

    for index, match in enumerate(matches):
        article_id = match.group(1)
        title = match.group(2).strip()

        start = match.start()
        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(text)
        )

        article_text = text[start:end].strip()

        articles.append(
            {
                "article_id": article_id,
                "title": title,
                "text": article_text,
            }
        )

    return articles


def chunk_articles(
    articles: list[dict],
    source: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[dict]:
    """
    Split each article into chunks and attach metadata.

    The PDF filename is included in chunk_id to ensure IDs are
    unique even when multiple PDFs contain the same article IDs.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be between 0 and chunk_size - 1"
        )

    # Convert PDF filename into a safe ID prefix.
    # Example: "account_authentication.pdf" -> "account_authentication"
    source_prefix = Path(source).stem

    chunks = []

    for article in articles:
        text = article["text"]

        start = 0
        chunk_number = 1

        while start < len(text):
            end = min(start + chunk_size, len(text))

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        # Example:
                        # account_authentication-KB-001-001
                        "chunk_id": (
                            f"{source_prefix}-"
                            f"{article['article_id']}-"
                            f"{chunk_number:03d}"
                        ),
                        "article_id": article["article_id"],
                        "title": article["title"],
                        "source": source,
                        "text": chunk_text,
                    }
                )

            if end >= len(text):
                break

            start = end - chunk_overlap
            chunk_number += 1

    return chunks