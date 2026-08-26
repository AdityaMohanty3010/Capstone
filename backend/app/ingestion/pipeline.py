from pathlib import Path

from app.embeddings.embedding_service import EmbeddingService
from app.ingestion.chunker import chunk_articles, split_into_articles
from app.ingestion.cleaner import clean_text
from app.ingestion.loader import load_pdf
from app.vectorstore.pinecone_services import PineconeService


class IngestionPipeline:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.pinecone_service = PineconeService()

    def ingest_folder(self, folder_path: str):

        folder = Path(folder_path)

        if not folder.exists():
            raise FileNotFoundError(
                f"Knowledge base folder not found: {folder_path}"
            )

        pdf_files = list(folder.glob("*.pdf"))

        if not pdf_files:
            raise ValueError(
                f"No PDF files found in: {folder_path}"
            )

        all_chunks = []

        print(f"\nFound {len(pdf_files)} PDF files.\n")

        for pdf_file in pdf_files:

            print(f"Processing: {pdf_file.name}")

            result = load_pdf(str(pdf_file))

            cleaned_text = clean_text(result["text"])

            articles = split_into_articles(cleaned_text)

            chunks = chunk_articles(
                articles=articles,
                source=result["source"],
                chunk_size=1000,
                chunk_overlap=200,
            )

            all_chunks.extend(chunks)

            print(f"  Articles found: {len(articles)}")
            print(f"  Chunks created: {len(chunks)}\n")

        print(f"Total chunks created: {len(all_chunks)}")

        return all_chunks

    def upload_chunks(
        self,
        chunks: list[dict],
        batch_size: int = 50,
    ):

        if not chunks:
            print("No chunks available to upload.")
            return

        total_chunks = len(chunks)
        total_uploaded = 0

        print("\nGenerating embeddings and uploading to Pinecone...\n")

        for start in range(0, total_chunks, batch_size):

            batch = chunks[start:start + batch_size]

            texts = [chunk["text"] for chunk in batch]

            embeddings = self.embedding_service.embed_texts(texts)

            vectors = []

            for chunk, embedding in zip(batch, embeddings):

                vectors.append(
                    {
                        "id": chunk["chunk_id"],
                        "values": embedding,
                        "metadata": {
                            "text": chunk["text"],
                            "source": chunk["source"],
                            "article_id": chunk["article_id"],
                            "title": chunk["title"],
                        },
                    }
                )

            self.pinecone_service.upsert_vectors(vectors)

            total_uploaded += len(vectors)

            print(
                f"Progress: {total_uploaded}/{total_chunks} "
                "vectors uploaded"
            )

        print("\nAll vectors uploaded successfully!")

    def ingest_and_upload(
        self,
        folder_path: str,
        clear_existing: bool = False,
    ):

        if clear_existing:
            self.pinecone_service.delete_all_vectors()

        chunks = self.ingest_folder(folder_path)

        self.upload_chunks(chunks)

        print("\nIngestion pipeline completed successfully!")

        return len(chunks)