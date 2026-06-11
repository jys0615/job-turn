from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_index_job():
    with patch("app.api.matching.ensure_collection"), \
         patch("app.api.matching.upsert_job"):
        response = client.post("/api/jobs/index", json={
            "job_id": 1,
            "title": "백엔드 개발자",
            "company": "(주)테스트",
            "description": "Spring Boot 개발",
            "requirements": "Java, Spring Boot 3년 이상",
        })
    assert response.status_code == 201
    assert response.json()["job_id"] == 1


def test_search_jobs():
    mock_results = [{"job_id": 1, "score": 0.92}, {"job_id": 2, "score": 0.85}]
    with patch("app.api.matching.search_jobs", return_value=mock_results):
        response = client.post("/api/jobs/search", json={
            "resume_text": "Python 백엔드 개발자 3년 경력",
            "top_k": 10,
        })
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["score"] == 0.92


def test_search_jobs_empty():
    with patch("app.api.matching.search_jobs", return_value=[]):
        response = client.post("/api/jobs/search", json={
            "resume_text": "이력서 텍스트",
        })
    assert response.status_code == 200
    assert response.json() == []
