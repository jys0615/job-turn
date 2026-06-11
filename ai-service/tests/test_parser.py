from unittest.mock import patch, MagicMock
from app.resume.parser import extract_sections, parse_pdf
import pytest


SAMPLE_MARKDOWN = """# 홍길동

## 자기소개
저는 3년차 백엔드 개발자입니다.

## 경력
- (주)테스트 2022~2024 백엔드 개발

## 기술스택
Python, FastAPI, Spring Boot, PostgreSQL

## 학력
한국대학교 컴퓨터공학과 졸업 (2022)

## 프로젝트
- JobTurn: AI 채용 매칭 서비스
"""


def test_extract_sections_all_found():
    sections = extract_sections(SAMPLE_MARKDOWN)
    assert "백엔드 개발자" in sections["summary"]
    assert "테스트" in sections["experience"]
    assert "Python" in sections["skills"]
    assert "한국대학교" in sections["education"]
    assert "JobTurn" in sections["projects"]


def test_extract_sections_raw_always_set():
    sections = extract_sections(SAMPLE_MARKDOWN)
    assert sections["raw"] == SAMPLE_MARKDOWN


def test_extract_sections_empty_input():
    sections = extract_sections("")
    assert sections["raw"] == ""
    assert sections["skills"] == ""


def test_extract_sections_no_headers():
    text = "이력서 내용입니다. 헤더가 없습니다."
    sections = extract_sections(text)
    assert sections["raw"] == text
    assert sections["experience"] == ""


def test_parse_pdf_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_pdf("/nonexistent/path/resume.pdf")


def test_parse_pdf_success():
    mock_text = "# 이력서\n\n## 경력\n테스트 경력"
    with patch("pymupdf4llm.to_markdown", return_value=mock_text):
        with patch("pathlib.Path.exists", return_value=True):
            result = parse_pdf("/fake/resume.pdf")
    assert result == mock_text.strip()
