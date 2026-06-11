"""
Qdrant Hybrid Search — Dense + BM25 (Sparse), RRF 스코어링
컬렉션: job_postings
"""
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, SparseVectorParams, SparseIndexParams,
    PointStruct, SparseVector, NamedVector, NamedSparseVector,
    SearchRequest, SearchParams, models,
)
from app.core.config import settings
from app.matching.embedder import embed

COLLECTION = "job_postings"
DENSE_DIM = 384  # BAAI/bge-small-en-v1.5


def get_client() -> QdrantClient:
    return QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)


def ensure_collection():
    client = get_client()
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION not in existing:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config={"dense": VectorParams(size=DENSE_DIM, distance=Distance.COSINE)},
            sparse_vectors_config={"sparse": SparseVectorParams(index=SparseIndexParams())},
        )


def upsert_job(job_id: int, title: str, company: str, description: str, requirements: str):
    """공고를 Qdrant에 저장한다 (Dense + Sparse)."""
    client = get_client()
    text = f"{title} {company} {description} {requirements}"
    dense_vec = embed(text)
    sparse_vec = _bm25_sparse(text)

    client.upsert(
        collection_name=COLLECTION,
        points=[
            PointStruct(
                id=job_id,
                vector={"dense": dense_vec, "sparse": sparse_vec},
                payload={"job_id": job_id, "title": title, "company": company},
            )
        ],
    )


def search_jobs(resume_text: str, top_k: int = 20) -> list[dict]:
    """이력서 텍스트로 공고를 Hybrid Search한다."""
    client = get_client()
    dense_vec = embed(resume_text)
    sparse_vec = _bm25_sparse(resume_text)

    results = client.query_points(
        collection_name=COLLECTION,
        prefetch=[
            models.Prefetch(query=dense_vec, using="dense", limit=top_k),
            models.Prefetch(query=models.SparseVector(**sparse_vec), using="sparse", limit=top_k),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=top_k,
    )

    return [
        {"job_id": p.payload["job_id"], "score": p.score}
        for p in results.points
    ]


def _bm25_sparse(text: str) -> dict:
    """간단한 TF 기반 Sparse 벡터 (BM25 근사)."""
    import math
    tokens = text.lower().split()
    tf: dict[int, float] = {}
    for token in tokens:
        idx = abs(hash(token)) % 30000
        tf[idx] = tf.get(idx, 0) + 1

    total = len(tokens) or 1
    indices = list(tf.keys())
    values = [math.log(1 + v / total) for v in tf.values()]
    return {"indices": indices, "values": values}
