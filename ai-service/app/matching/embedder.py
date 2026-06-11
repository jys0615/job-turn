"""
텍스트 임베딩 — Anthropic Embeddings 대신 fastembed (경량, 로컬)
Dense: BAAI/bge-small-en-v1.5 (다국어 지원)
"""
from fastembed import TextEmbedding

_model: TextEmbedding | None = None


def get_model() -> TextEmbedding:
    global _model
    if _model is None:
        _model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return _model


def embed(text: str) -> list[float]:
    model = get_model()
    vectors = list(model.embed([text]))
    return vectors[0].tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    model = get_model()
    return [v.tolist() for v in model.embed(texts)]
