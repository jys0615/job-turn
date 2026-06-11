from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_success():
    mock_result = {
        "match_score": 75,
        "match_reason": "Python 및 FastAPI 경험이 요구 사항과 일치합니다.",
        "skill_gaps": ["Kubernetes", "Kafka"],
        "resume_suggestion": "Kubernetes 경험을 추가하면 합격 가능성이 높아집니다.",
    }
    with patch("app.api.analyze.analyze_match", return_value=mock_result):
        response = client.post("/api/analyze", json={
            "resume_text": "Python 개발자, FastAPI 경험 2년",
            "job_description": "백엔드 개발자 채용",
            "job_requirements": "Python, FastAPI, Kubernetes",
        })
    assert response.status_code == 200
    data = response.json()
    assert data["match_score"] == 75
    assert "Kubernetes" in data["skill_gaps"]


def test_analyze_missing_field():
    response = client.post("/api/analyze", json={
        "resume_text": "이력서",
        # job_description 누락
        "job_requirements": "Python",
    })
    assert response.status_code == 422
