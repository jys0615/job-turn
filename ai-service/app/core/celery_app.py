from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "jobturn",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.crawler.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Seoul",
    beat_schedule={
        "crawl-saramin-every-6h": {
            "task": "app.crawler.tasks.crawl_saramin",
            "schedule": 21600,  # 6 hours
        }
    },
)
