"""
DB에 있는 공고를 Qdrant에 벡터 색인하는 스크립트

실행: python scripts/index_jobs_to_qdrant.py
환경변수: DATABASE_URL, QDRANT_HOST (없으면 로컬 기본값)
"""
import os
import sys
import psycopg2

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ai-service"))

DB_URL = os.getenv("DATABASE_URL", "postgresql://jobturn:jobturn@localhost:5432/jobturn")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")


def main():
    from app.matching.qdrant_store import ensure_collection, upsert_job
    from app.core.config import settings

    # 환경변수 오버라이드
    settings.qdrant_host = QDRANT_HOST

    print("Qdrant 컬렉션 초기화...")
    ensure_collection()

    print(f"DB에서 공고 로드 중: {DB_URL.split('@')[-1]}")
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, company,
               COALESCE(description, ''), COALESCE(requirements, '')
        FROM job_postings
        WHERE expired_at IS NULL OR expired_at >= CURRENT_DATE
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print(f"총 {len(rows)}개 공고 색인 시작...")
    for i, (job_id, title, company, description, requirements) in enumerate(rows):
        upsert_job(job_id, title, company, description, requirements)
        if (i + 1) % 10 == 0:
            print(f"  {i + 1}/{len(rows)} 완료")

    print(f"✅ Qdrant 색인 완료: {len(rows)}건")


if __name__ == "__main__":
    main()
