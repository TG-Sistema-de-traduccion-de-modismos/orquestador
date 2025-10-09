import requests
from app.core.config import settings

class OrchestratorService:
    @staticmethod
    def analyze_text(text: str):
        beto = requests.post(settings.BETO_URL, json={"text": text}, timeout=30).json()
        phi_payload = {"frase": text, "significado": beto.get("modismos_detectados", {})}
        phi = requests.post(settings.PHI_URL, json=phi_payload, timeout=30).json()
        return {"text": text, "beto": beto, "phi": phi}

    @staticmethod
    def analyze_audio(file_bytes: bytes, filename: str, content_type: str):
        if not content_type:
            content_type = "audio/wav"  # fallback seguro

        whisper_url = f"{settings.WHISPER_URL}/transcribe"
        files = {"file": (filename, file_bytes, content_type)}

        response = requests.post(whisper_url, files=files, timeout=60)
        if response.status_code != 200:
            raise Exception(f"Error al transcribir audio: {response.text}")

        whisper = response.json()
        text = whisper.get("transcription", "")
        return OrchestratorService.analyze_text(text)
