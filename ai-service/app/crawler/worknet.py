"""
고용노동부 워크넷 채용정보 Open API 크롤러
API 문서: https://www.work.go.kr/opi/openApiIntroduce.do
"""
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterator

WORKNET_BASE_URL = "https://www.work.go.kr/opi/opi/opia/wantedApi.do"


def _parse_job(item: ET.Element) -> dict | None:
    def text(tag: str) -> str:
        el = item.find(tag)
        return el.text.strip() if el is not None and el.text else ""

    wanted_auth_no = text("wantedAuthNo")
    if not wanted_auth_no:
        return None

    expire_raw = text("receiptCloseDt")
    expired_at = None
    if expire_raw and len(expire_raw) == 8:
        try:
            expired_at = datetime.strptime(expire_raw, "%Y%m%d").date().isoformat()
        except ValueError:
            pass

    return {
        "external_id": f"WN-{wanted_auth_no}",
        "source": "WORKNET",
        "title": text("title"),
        "company": text("company"),
        "location": text("workRegionNm"),
        "description": text("jobsNm"),
        "requirements": text("requireCareerNm"),
        "experience_level": text("requireCareerNm"),
        "expired_at": expired_at,
        "original_url": f"https://www.work.go.kr/empInfo/empInfoSrch/detail/empDetailAuthView.do?wantedAuthNo={wanted_auth_no}",
        "skills": [],
    }


def fetch_jobs(api_key: str, keyword: str = "", page: int = 1, page_size: int = 100) -> Iterator[dict]:
    """워크넷 API에서 채용 공고를 가져온다."""
    params = {
        "authKey": api_key,
        "callTp": "L",
        "returnType": "XML",
        "startPage": page,
        "display": page_size,
        "keyword": keyword,
    }
    response = httpx.get(WORKNET_BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    for item in root.findall(".//wanted"):
        job = _parse_job(item)
        if job:
            yield job


def fetch_all_pages(api_key: str, keyword: str = "", max_pages: int = 10) -> list[dict]:
    """여러 페이지에 걸쳐 공고를 수집한다."""
    jobs = []
    for page in range(1, max_pages + 1):
        page_jobs = list(fetch_jobs(api_key, keyword, page=page))
        if not page_jobs:
            break
        jobs.extend(page_jobs)
    return jobs
