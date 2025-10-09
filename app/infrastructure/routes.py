from fastapi import APIRouter, UploadFile, File, HTTPException
from app.application.services import OrchestratorService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze-text")
async def analyze_text(payload: dict):
    try:
        text = payload.get("text")
        if not text:
            raise ValueError("El campo 'text' es obligatorio")
        result = OrchestratorService.analyze_text(text)
        return result
    except Exception as e:
        logger.error(f"Error en pipeline de texto: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    try:
        result = OrchestratorService.analyze_audio(await file.read(), file.filename, file.content_type)
        return result
    except Exception as e:
        logger.error(f"Error en pipeline de audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))
