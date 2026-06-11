from fastapi import APIRouter
from pydantic import BaseModel
from app.matching.qdrant_store import search_jobs, upsert_job, ensure_collection
from app.llm.analyzer import analyze_match

router = APIRouter()


class JobIndexRequest(BaseModel):
    job_id: int
    title: str
    company: str
    description: str
    requirements: str


class SearchRequest(BaseModel):
    resume_text: str
    top_k: int = 20


class SearchResult(BaseModel):
    job_id: int
    score: float


class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str
    job_requirements: str


@router.post("/jobs/index", status_code=201)
def index_job(request: JobIndexRequest):
    """공고를 Qdrant에 색인한다."""
    ensure_collection()
    upsert_job(
        request.job_id, request.title, request.company,
        request.description, request.requirements,
    )
    return {"status": "indexed", "job_id": request.job_id}


@router.post("/jobs/search", response_model=list[SearchResult])
def search(request: SearchRequest):
    """이력서로 유사 공고를 Hybrid Search한다."""
    results = search_jobs(request.resume_text, top_k=request.top_k)
    return [SearchResult(**r) for r in results]
