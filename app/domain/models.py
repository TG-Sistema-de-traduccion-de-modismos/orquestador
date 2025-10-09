from pydantic import BaseModel

class BetoResponse(BaseModel):
    modismos_detectados: dict
    confidence: float | None = None

class PhiResponse(BaseModel):
    frase_neutralizada: str
    cambios: list[str] | None = None

class OrchestratorResult(BaseModel):
    original_text: str
    beto_result: BetoResponse
    phi_result: PhiResponse
    status: str
