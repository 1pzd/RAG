from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "IoT-RAG-QA"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.deepseek.com"
    LLM_MODEL_NAME: str = "deepseek-v4-pro"
    LLM_TEMPERATURE: float = 1.0
    LLM_MAX_TOKENS: int = 4096

    EMBEDDING_MODEL_NAME: str = "text-embedding-3-small"
    EMBEDDING_DIMENSION: int = 1536

    VECTOR_DB_BACKEND: str = "chromadb"
    CHROMA_PERSIST_DIR: Path = Path("./data/chroma_db")
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_NAME: str = "iot_knowledge"
    QDRANT_API_KEY: str = ""

    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64
    TOP_K: int = 5

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["http://localhost:8501"]


settings = Settings()
