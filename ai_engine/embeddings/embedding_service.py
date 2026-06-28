from __future__ import annotations

from typing import Any


class EmbeddingService:
    """Generate semantic embeddings with SentenceTransformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self.dimension = 384
        self.model_version = "1.0"
        self._model: Any | None = None

    def _get_model(self) -> Any:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed_text(self, text: str) -> list[float]:
        cleaned_text = (text or "").strip()
        model = self._get_model()
        vector = model.encode(cleaned_text, normalize_embeddings=True)
        return [float(value) for value in vector]

