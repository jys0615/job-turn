from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import tempfile
import os
from app.resume.parser import parse_pdf, extract_sections

router = APIRouter()


class ParseResponse(BaseModel):
    raw: str
    summary: str
    experience: str
    skills: str
    education: str
    projects: str


@router.post("/resume/parse", response_model=ParseResponse)
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드할 수 있습니다.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        markdown_text = parse_pdf(tmp_path)
        sections = extract_sections(markdown_text)
        return ParseResponse(**sections)
    finally:
        os.unlink(tmp_path)
