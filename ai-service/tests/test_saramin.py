from unittest.mock import patch, MagicMock
from app.crawler.saramin import _parse_job, fetch_jobs


def make_job(job_id="12345", title="백엔드 개발자", company="(주)테스트",
             location="서울", experience="경력 3년", expire="2025-12-31"):
    return {
        "id": job_id,
        "url": f"https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx={job_id}",
        "active": 1,
        "expiration-date": expire,
        "company": {"detail": {"name": company}},
        "position": {
            "title": title,
            "location": {"name": location},
            "experience-level": {"name": experience},
            "required-education-level": {"name": "대졸"},
            "job-category": {"name": "IT개발·데이터"},
        },
        "salary": {"name": "회사내규에 따름"},
    }


def test_parse_job_success():
    job = make_job()
    result = _parse_job(job)
    assert result["external_id"] == "SR-12345"
    assert result["source"] == "SARAMIN"
    assert result["title"] == "백엔드 개발자"
    assert result["company"] == "(주)테스트"
    assert result["expired_at"] == "2025-12-31"


def test_parse_job_missing_fields():
    result = _parse_job({})
    assert result["external_id"] == "SR-"
    assert result["title"] == ""
    assert result["skills"] == []


def test_fetch_jobs_parses_response():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "jobs": {
            "count": 1,
            "start": 1,
            "total": 1,
            "job": [make_job("99999", "파이썬 개발자", "테스트사")]
        }
    }
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        jobs = list(fetch_jobs("test-api-key", keywords="Python"))

    assert len(jobs) == 1
    assert jobs[0]["external_id"] == "SR-99999"
    assert jobs[0]["title"] == "파이썬 개발자"


def test_fetch_jobs_empty_response():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"jobs": {"count": 0, "job": []}}
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        jobs = list(fetch_jobs("test-api-key"))

    assert jobs == []
