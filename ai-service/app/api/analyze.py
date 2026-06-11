from fastapi import APIRouter
from pydantic import BaseModel
from app.llm.analyzer import analyze_match

router = APIRouter()


class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str
    job_requirements: str


class AnalyzeResponse(BaseModel):
    match_score: int
    match_reason: str
    skill_gaps: list[str]
    resume_suggestion: str


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    result = analyze_match(
        request.resume_text,
        request.job_description,
        request.job_requirements,
    )
    return AnalyzeResponse(**result)
