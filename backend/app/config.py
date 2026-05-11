"""Runtime configuration for the backend."""

from functools import lru_cache
from pathlib import Path
import os


class Settings:
    app_name = "payments-platform-navigator"
    data_classification = "synthetic"
    port = int(os.getenv("PORT", "8080"))
    host = "0.0.0.0"
    backend_dir = Path(__file__).resolve().parents[1]
    repo_root = backend_dir.parent
    data_dir = repo_root / "data"
    container_static_dir = repo_root / "static"
    local_frontend_dist_dir = repo_root / "frontend" / "dist"
    cors_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # AI configuration (Phase 9C)
    enable_ai_explanations = os.getenv("ENABLE_AI_EXPLANATIONS", "false").lower() == "true"
    ai_provider = os.getenv("AI_PROVIDER", "none").lower()
    ai_model = os.getenv("AI_MODEL", "none")
    google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
    google_cloud_location = os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west2")


@lru_cache
def get_settings() -> Settings:
    return Settings()
