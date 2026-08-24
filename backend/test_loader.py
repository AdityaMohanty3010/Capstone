from app.ingestion.loader import load_pdf
from app.ingestion.cleaner import clean_text
from app.ingestion.chunker import chunk_text


pdf_path = "../knowledge_base/test/sample.pdf"

result = load_pdf(pdf_path)

raw_text = result["text"]
cleaned_text = clean_text(raw_text)

chunks = chunk_text(
    cleaned_text,
    chunk_size=1000,
    chunk_overlap=200
)

print("Source:", result["source"])
print("Raw characters:", len(raw_text))
print("Cleaned characters:", len(cleaned_text))
print("Number of chunks:", len(chunks))

print("\n--- FIRST CHUNK ---\n")
print(chunks[0])

print("\n--- SECOND CHUNK ---\n")
print(chunks[1] if len(chunks) > 1 else "No second chunk")