"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
	ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
	ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2")
	data_dir: Path = Path(os.getenv("DATA_DIR", ".data"))
	chunk_size: int = int(os.getenv("CHUNK_SIZE", "1200"))
	chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "180"))


settings = Settings()
