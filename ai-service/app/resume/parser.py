"""
이력서 PDF 파싱 — pymupdf4llm
PDF → Markdown 변환 후 Claude가 읽기 최적화된 구조로 반환
"""
import pymupdf4llm
from pathlib import Path


def parse_pdf(file_path: str) -> str:
    """PDF 파일을 Markdown 텍스트로 변환한다."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    md_text = pymupdf4llm.to_markdown(str(path))
    return md_text.strip()


def extract_sections(markdown_text: str) -> dict:
    """
    Markdown에서 주요 섹션을 추출한다.
    섹션 헤더(#, ##)를 기준으로 분리.
    """
    sections = {
        "raw": markdown_text,
        "summary": "",
        "experience": "",
        "skills": "",
        "education": "",
        "projects": "",
    }

    keyword_map = {
        "summary": ["자기소개", "소개", "summary", "about", "profile"],
        "experience": ["경력", "경험", "work experience", "experience", "직무경력"],
        "skills": ["기술", "스킬", "skills", "tech stack", "기술스택", "사용기술"],
        "education": ["학력", "education", "학교"],
        "projects": ["프로젝트", "project", "포트폴리오"],
    }

    lines = markdown_text.split("\n")
    current_section = None
    buffer = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            if current_section and buffer:
                sections[current_section] = "\n".join(buffer).strip()
            buffer = []
            current_section = None
            header_text = stripped.lstrip("#").strip().lower()
            for section, keywords in keyword_map.items():
                if any(kw in header_text for kw in keywords):
                    current_section = section
                    break
        elif current_section:
            buffer.append(line)

    if current_section and buffer:
        sections[current_section] = "\n".join(buffer).strip()

    return sections
