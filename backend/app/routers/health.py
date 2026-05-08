from fastapi import APIRouter

from ..config import get_settings
from ..data_loader import get_knowledge_data

router = APIRouter()


@router.get("/health")
def health() -> dict:
    data = get_knowledge_data()
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.app_name,
        "data_classification": settings.data_classification,
        "data_files_loaded": data.data_files_loaded,
    }
