import re


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
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)

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
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be between 0 and chunk_size - 1"
        )

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
                        "chunk_id": f"{article['article_id']}-{chunk_number:03d}",
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