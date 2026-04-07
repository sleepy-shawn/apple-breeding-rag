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
    qdrant_genes_firmness_collection: str = "genes_firmness"
    qdrant_genes_color_collection: str = "genes_color"
    qdrant_genes_acidity_collection: str = "genes_acidity"
    qdrant_genes_harvest_collection: str = "genes_harvest"
    qdrant_genes_sugar_collection: str = "genes_sugar"
    qdrant_genes_gdr_collection: str = "genes_gdr"
    qdrant_genes_gdr_curated_collection: str = "genes_gdr_curated"
    qdrant_genes_gdr_firmness_collection: str = "genes_gdr_firmness"
    qdrant_genes_gdr_color_collection: str = "genes_gdr_color"
    qdrant_genes_gdr_acidity_collection: str = "genes_gdr_acidity"
    qdrant_genes_gdr_harvest_collection: str = "genes_gdr_harvest"
    qdrant_genes_gdr_sugar_collection: str = "genes_gdr_sugar"
    qdrant_genes_gdr_curated_firmness_collection: str = "genes_gdr_curated_firmness"
    qdrant_genes_gdr_curated_color_collection: str = "genes_gdr_curated_color"
    qdrant_genes_gdr_curated_acidity_collection: str = "genes_gdr_curated_acidity"
    qdrant_genes_gdr_curated_harvest_collection: str = "genes_gdr_curated_harvest"
    qdrant_genes_gdr_curated_sugar_collection: str = "genes_gdr_curated_sugar"
    auto_ingest_on_startup: bool = Field(default=True, alias="AUTO_INGEST_ON_STARTUP")
    auto_ingest_genes_filename: str = Field(default="genes.csv", alias="AUTO_INGEST_GENES_FILENAME")
    auto_ingest_genes_firmness_filename: str = Field(
        default="genes_firmness_curated.csv",
        alias="AUTO_INGEST_GENES_FIRMNESS_FILENAME",
    )
    auto_ingest_genes_color_filename: str = Field(
        default="genes_color_curated.csv",
        alias="AUTO_INGEST_GENES_COLOR_FILENAME",
    )
    auto_ingest_genes_acidity_filename: str = Field(
        default="genes_acidity_curated.csv",
        alias="AUTO_INGEST_GENES_ACIDITY_FILENAME",
    )
    auto_ingest_genes_harvest_filename: str = Field(
        default="genes_harvest_curated.csv",
        alias="AUTO_INGEST_GENES_HARVEST_FILENAME",
    )
    auto_ingest_genes_sugar_filename: str = Field(
        default="genes_sugar_curated.csv",
        alias="AUTO_INGEST_GENES_SUGAR_FILENAME",
    )
    auto_ingest_genes_gdr_filename: str = Field(
        default="genes_gdr.csv",
        alias="AUTO_INGEST_GENES_GDR_FILENAME",
    )
    auto_ingest_genes_gdr_curated_filename: str = Field(
        default="genes_gdr_curated.csv",
        alias="AUTO_INGEST_GENES_GDR_CURATED_FILENAME",
    )
    auto_ingest_genes_gdr_firmness_filename: str = Field(
        default="genes_gdr_firmness.csv",
        alias="AUTO_INGEST_GENES_GDR_FIRMNESS_FILENAME",
    )
    auto_ingest_genes_gdr_color_filename: str = Field(
        default="genes_gdr_color.csv",
        alias="AUTO_INGEST_GENES_GDR_COLOR_FILENAME",
    )
    auto_ingest_genes_gdr_acidity_filename: str = Field(
        default="genes_gdr_acidity.csv",
        alias="AUTO_INGEST_GENES_GDR_ACIDITY_FILENAME",
    )
    auto_ingest_genes_gdr_harvest_filename: str = Field(
        default="genes_gdr_harvest.csv",
        alias="AUTO_INGEST_GENES_GDR_HARVEST_FILENAME",
    )
    auto_ingest_genes_gdr_sugar_filename: str = Field(
        default="genes_gdr_sugar.csv",
        alias="AUTO_INGEST_GENES_GDR_SUGAR_FILENAME",
    )
    auto_ingest_genes_gdr_curated_firmness_filename: str = Field(
        default="genes_gdr_curated_firmness.csv",
        alias="AUTO_INGEST_GENES_GDR_CURATED_FIRMNESS_FILENAME",
    )
    auto_ingest_genes_gdr_curated_color_filename: str = Field(
        default="genes_gdr_curated_color.csv",
        alias="AUTO_INGEST_GENES_GDR_CURATED_COLOR_FILENAME",
    )
    auto_ingest_genes_gdr_curated_acidity_filename: str = Field(
        default="genes_gdr_curated_acidity.csv",
        alias="AUTO_INGEST_GENES_GDR_CURATED_ACIDITY_FILENAME",
    )
    auto_ingest_genes_gdr_curated_harvest_filename: str = Field(
        default="genes_gdr_curated_harvest.csv",
        alias="AUTO_INGEST_GENES_GDR_CURATED_HARVEST_FILENAME",
    )
    auto_ingest_genes_gdr_curated_sugar_filename: str = Field(
        default="genes_gdr_curated_sugar.csv",
        alias="AUTO_INGEST_GENES_GDR_CURATED_SUGAR_FILENAME",
    )

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
