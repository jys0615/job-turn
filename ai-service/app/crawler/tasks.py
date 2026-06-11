import logging
from app.core.celery_app import celery_app
from app.core.config import settings
from app.crawler.saramin import fetch_all_pages

logger = logging.getLogger(__name__)


@celery_app.task(name="app.crawler.tasks.crawl_saramin", bind=True, max_retries=3)
def crawl_saramin(self, keywords: str = ""):
    """사람인 공고를 수집하고 DB에 저장한다."""
    try:
        if not settings.saramin_api_key:
            logger.warning("SARAMIN_API_KEY not set, skipping crawl")
            return {"status": "skipped", "reason": "no api key"}

        jobs = fetch_all_pages(settings.saramin_api_key, keywords=keywords)
        saved = _save_jobs(jobs)
        logger.info("Saramin crawl complete: %d jobs saved", saved)
        return {"status": "ok", "saved": saved}
    except Exception as exc:
        logger.error("Saramin crawl failed: %s", exc)
        raise self.retry(exc=exc, countdown=60)


def _save_jobs(jobs: list[dict]) -> int:
    """DB 저장 (동기 방식 — Celery worker 환경)."""
    import psycopg2

    db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    saved = 0
    try:
        for job in jobs:
            cur.execute(
                """
                INSERT INTO job_postings
                    (external_id, source, title, company, location, description,
                     requirements, experience_level, expired_at, original_url, created_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
                ON CONFLICT (external_id) DO NOTHING
                """,
                (
                    job["external_id"], job["source"], job["title"], job["company"],
                    job["location"], job["description"], job["requirements"],
                    job["experience_level"], job["expired_at"], job["original_url"],
                ),
            )
            saved += cur.rowcount
        conn.commit()
    finally:
        cur.close()
        conn.close()
    return saved
