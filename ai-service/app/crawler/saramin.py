"""
사람인 채용정보 Open API 크롤러
API 문서: https://oapi.saramin.co.kr/guide/job-search
"""
import httpx
from typing import Iterator

SARAMIN_BASE_URL = "https://oapi.saramin.co.kr/job-search"


def _parse_job(job: dict) -> dict:
    position = job.get("position", {})
    company = job.get("company", {})
    salary = job.get("salary", {})
    location = position.get("location", {})

    return {
        "external_id": f"SR-{job.get('id', '')}",
        "source": "SARAMIN",
        "title": position.get("title", ""),
        "company": company.get("detail", {}).get("name", ""),
        "location": location.get("name", ""),
        "description": position.get("job-category", {}).get("name", ""),
        "requirements": position.get("required-education-level", {}).get("name", ""),
        "experience_level": position.get("experience-level", {}).get("name", ""),
        "expired_at": job.get("expiration-date", None),
        "original_url": job.get("url", ""),
        "skills": [],
    }


def fetch_jobs(api_key: str, keywords: str = "", start: int = 1, count: int = 100) -> Iterator[dict]:
    """사람인 API에서 채용 공고를 가져온다."""
    params = {
        "access-key": api_key,
        "keywords": keywords,
        "start": start,
        "count": count,
        "job_type": 1,  # 정규직
    }
    headers = {"Accept": "application/json"}
    response = httpx.get(SARAMIN_BASE_URL, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    jobs = data.get("jobs", {}).get("job", [])
    for job in jobs:
        yield _parse_job(job)


def fetch_all_pages(api_key: str, keywords: str = "", max_pages: int = 10) -> list[dict]:
    """여러 페이지에 걸쳐 공고를 수집한다."""
    jobs = []
    count = 100
    for page in range(max_pages):
        start = page * count + 1
        page_jobs = list(fetch_jobs(api_key, keywords, start=start, count=count))
        if not page_jobs:
            break
        jobs.extend(page_jobs)
    return jobs
