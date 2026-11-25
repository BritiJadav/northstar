import os
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseModel):
    APP_NAME: str = "NorthStar Commercial Lines Ingestion & Triage Gateway"
    VERSION: str = "1.0.0"
    ENV: str = os.getenv("APP_ENV", "development")
    
    # GCP & AI Gateway (In-Region Mumbai Constraint)
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "northstar-demo")
    GCP_REGION: str = os.getenv("GCP_REGION", "asia-south1")
    MODEL_NAME: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Storage Paths
    DATA_DIR: Path = BASE_DIR / "data"
    DB_PATH: Path = BASE_DIR / "data" / "northstar_audit.db"
    STORAGE_DIR: Path = BASE_DIR / "data" / "submissions"
    
    # Governance & Security Gates
    ENABLE_PROMPT_INJECTION_SCAN: bool = True
    ENABLE_DPDP_MASKING: bool = True
    MAX_ATTACHMENT_SIZE_MB: int = 25
    
    # Duplicate Threshold (0.0 to 1.0)
    DUPLICATE_SIMILARITY_THRESHOLD: float = 0.82

settings = Settings()

# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
