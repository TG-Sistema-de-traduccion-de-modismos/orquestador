from fastapi import FastAPI
from app.infrastructure.routes import router
from app.core.logging_config import setup_logging
from app.core.config import settings

setup_logging()

app = FastAPI(
    title="Orquestador - Modismos",
    version="2.0",
    description="Orquesta Whisper, BETO y PHI para analizar modismos"
)

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "orquestador", "version": settings.VERSION}
