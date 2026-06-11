import xml.etree.ElementTree as ET
from app.crawler.worknet import _parse_job, fetch_jobs
from unittest.mock import patch, MagicMock


def make_item(wanted_auth_no="20240001", title="백엔드 개발자", company="(주)테스트",
              region="서울", jobs_nm="Python, Django", career="경력 3년", expire="20250101"):
    xml_str = f"""<wanted>
        <wantedAuthNo>{wanted_auth_no}</wantedAuthNo>
        <title>{title}</title>
        <company>{company}</company>
        <workRegionNm>{region}</workRegionNm>
        <jobsNm>{jobs_nm}</jobsNm>
        <requireCareerNm>{career}</requireCareerNm>
        <receiptCloseDt>{expire}</receiptCloseDt>
    </wanted>"""
    return ET.fromstring(xml_str)


def test_parse_job_success():
    item = make_item()
    result = _parse_job(item)
    assert result is not None
    assert result["external_id"] == "WN-20240001"
    assert result["source"] == "WORKNET"
    assert result["title"] == "백엔드 개발자"
    assert result["company"] == "(주)테스트"
    assert result["expired_at"] == "2025-01-01"


def test_parse_job_missing_id_returns_none():
    xml_str = "<wanted><title>공고</title></wanted>"
    item = ET.fromstring(xml_str)
    assert _parse_job(item) is None


def test_parse_job_invalid_date():
    item = make_item(expire="INVALID")
    result = _parse_job(item)
    assert result is not None
    assert result["expired_at"] is None


def test_fetch_jobs_parses_response():
    xml_response = """<?xml version="1.0"?>
    <wantedRoot>
        <wanted>
            <wantedAuthNo>12345</wantedAuthNo>
            <title>백엔드</title>
            <company>테스트사</company>
            <workRegionNm>서울</workRegionNm>
            <jobsNm>Python</jobsNm>
            <requireCareerNm>신입</requireCareerNm>
            <receiptCloseDt>20251231</receiptCloseDt>
        </wanted>
    </wantedRoot>"""

    mock_resp = MagicMock()
    mock_resp.text = xml_response
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        jobs = list(fetch_jobs("test-api-key", keyword="Python"))

    assert len(jobs) == 1
    assert jobs[0]["external_id"] == "WN-12345"
