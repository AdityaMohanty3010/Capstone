from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ingestion.pipeline import IngestionPipeline


router = APIRouter(prefix="/api", tags=["Ingestion"])

ingestion_pipeline = IngestionPipeline()


class IngestRequest(BaseModel):
    folder_path: str
    clear_existing: bool = False


class IngestResponse(BaseModel):
    message: str
    chunks_created: int


@router.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest):

    try:
        chunks_created = ingestion_pipeline.ingest_and_upload(
            folder_path=request.folder_path,
            clear_existing=request.clear_existing,
        )

        return IngestResponse(
            message="Ingestion completed successfully",
            chunks_created=chunks_created,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )