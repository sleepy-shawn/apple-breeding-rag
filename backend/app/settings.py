from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

TRAITS = ("firmness", "color", "acidity", "harvest", "sugar")
COLLECTION_TIERS = ("curated", "gdr", "gdr_curated")


def _build_collection_registry() -> dict[str, str]:
    registry: dict[str, str] = {
        "papers": "papers",
        "genes": "genes",
    }
    for trait in TRAITS:
        registry[f"genes_{trait}"] = f"genes_{trait}"
    registry["genes_gdr"] = "genes_gdr"
    registry["genes_gdr_curated"] = "genes_gdr_curated"
    for trait in TRAITS:
        registry[f"genes_gdr_{trait}"] = f"genes_gdr_{trait}"
        registry[f"genes_gdr_curated_{trait}"] = f"genes_gdr_curated_{trait}"
    return registry


COLLECTION_REGISTRY: dict[str, str] = _build_collection_registry()

DEFAULT_INGEST_FILENAMES: dict[str, str] = {
    "genes": "genes.csv",
    **{f"genes_{t}": f"genes_{t}_curated.csv" for t in TRAITS},
    "genes_gdr": "genes_gdr.csv",
    "genes_gdr_curated": "genes_gdr_curated.csv",
    **{f"genes_gdr_{t}": f"genes_gdr_{t}.csv" for t in TRAITS},
    **{f"genes_gdr_curated_{t}": f"genes_gdr_curated_{t}.csv" for t in TRAITS},
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Apple Breeding RAG API"
    api_prefix: str = "/api"

    qdrant_url: str = Field(default="http://qdrant:6333", alias="QDRANT_URL")
    auto_ingest_on_startup: bool = Field(default=True, alias="AUTO_INGEST_ON_STARTUP")

    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="EMBEDDING_MODEL",
    )

    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    llm_base_url: str = Field(default="https://api.deepseek.com", alias="LLM_BASE_URL")
    llm_model: str = Field(default="deepseek-chat", alias="LLM_MODEL")

    def collection_name(self, key: str) -> str:
        if key not in COLLECTION_REGISTRY:
            raise ValueError(f"Unknown collection key: {key}")
        return COLLECTION_REGISTRY[key]

    def ingest_filename(self, key: str) -> str:
        return DEFAULT_INGEST_FILENAMES.get(key, f"{key}.csv")

    def trait_collections(self, trait: str | None) -> list[str]:
        if trait and trait in TRAITS:
            return [
                self.collection_name(f"genes_{trait}"),
                self.collection_name(f"genes_gdr_curated_{trait}"),
                self.collection_name("genes_gdr_curated"),
                self.collection_name(f"genes_gdr_{trait}"),
                self.collection_name("genes_gdr"),
            ]
        return [
            self.collection_name("genes_gdr_curated"),
            self.collection_name("genes_gdr"),
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
