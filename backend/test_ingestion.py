from pathlib import Path

from app.api.ingest import IngestionPipeline


project_root = Path(__file__).resolve().parent.parent
knowledge_base_path = project_root / "knowledge_base"


pipeline = IngestionPipeline()

total_chunks = pipeline.ingest_and_upload(
    folder_path=str(knowledge_base_path),
    clear_existing=True,
)

print(f"\nTotal vectors uploaded: {total_chunks}")