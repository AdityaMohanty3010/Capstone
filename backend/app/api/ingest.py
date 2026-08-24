from fastapi import APIRouter

router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"]
)


@router.get("/test")
def test_ingestion():
    return {
        "message": "Ingestion endpoint is working"
    }