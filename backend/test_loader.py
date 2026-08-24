from app.ingestion.loader import load_pdf
from app.ingestion.cleaner import clean_text
from app.ingestion.chunker import (
    split_into_articles,
    chunk_articles,
)


pdf_path = "../knowledge_base/test/sample.pdf"

result = load_pdf(pdf_path)

cleaned_text = clean_text(result["text"])

articles = split_into_articles(cleaned_text)

chunks = chunk_articles(
    articles,
    source=result["source"],
    chunk_size=1000,
    chunk_overlap=200,
)

print("Source:", result["source"])
print("Total articles:", len(articles))
print("Total chunks:", len(chunks))

print("\n--- FIRST CHUNK ---\n")

first_chunk = chunks[0]

print("Chunk ID:", first_chunk["chunk_id"])
print("Article ID:", first_chunk["article_id"])
print("Title:", first_chunk["title"])
print("Source:", first_chunk["source"])
print("Characters:", len(first_chunk["text"]))

print("\nChunk text:\n")
print(first_chunk["text"])