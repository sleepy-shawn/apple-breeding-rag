from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Apple Breeding RAG API"
    api_prefix: str = "/api"

    qdrant_url: str = Field(default="http://qdrant:6333", alias="QDRANT_URL")
    qdrant_papers_collection: str = "papers"
    qdrant_genes_collection: str = "genes"
    auto_ingest_on_startup: bool = Field(default=True, alias="AUTO_INGEST_ON_STARTUP")
    auto_ingest_genes_filename: str = Field(default="genes.csv", alias="AUTO_INGEST_GENES_FILENAME")

    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="EMBEDDING_MODEL",
    )

    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    llm_base_url: str = Field(default="https://api.deepseek.com", alias="LLM_BASE_URL")
    llm_model: str = Field(default="deepseek-chat", alias="LLM_MODEL")


@lru_cache
def get_settings() -> Settings:
    return Settings()
