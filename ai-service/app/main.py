from fastapi import FastAPI
from prometheus_client import make_asgi_app

from app.api.analyze import router as analyze_router

app = FastAPI(title="JobTurn AI Service", version="0.1.0")

app.include_router(analyze_router, prefix="/api")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/health")
def health():
    return {"status": "ok"}
