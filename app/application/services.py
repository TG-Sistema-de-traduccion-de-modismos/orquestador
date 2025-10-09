import requests
from app.core.config import settings

class OrchestratorService:

    @staticmethod
    def analyze_text(text: str):
        """
        Analiza texto usando BETO y PHI.
        Devuelve un JSON consolidado con el análisis y estado de los servicios.
        """
        try:
            beto_response = requests.post(settings.BETO_URL, json={"text": text}, timeout=30)
            beto_result = beto_response.json() if beto_response.status_code == 200 else {}
            beto_available = beto_response.status_code == 200

            phi_response = requests.post(
                settings.PHI_URL,
                json={"frase": text, "significado": beto_result.get("modismos_detectados", {})},
                timeout=30
            )
            phi_result = phi_response.json() if phi_response.status_code == 200 else {}
            phi_available = phi_response.status_code == 200

            response = {
                "original_text": beto_result.get("texto_original", text),
                "analysis": f"Análisis completado con BETO-Finetuned: {beto_result.get('total_modismos', 0)} modismos detectados",
                "modismos_detected": beto_result.get("modismos_detectados", {}),
                "modismos_detallados": beto_result.get("modismos_detallados", []),
                "total_modismos": beto_result.get("total_modismos", 0),
                "frase_neutral": phi_result.get("neutralizada", text),
                "status": "success" if (beto_available and phi_available) else "partial_success",
                "beto_available": beto_available,
                "phi_available": phi_available,
                "beto_response": beto_result,
                "phi_response": phi_result,
            }

            return response

        except Exception as e:
            return {
                "original_text": text,
                "analysis": f"Error: {str(e)}",
                "modismos_detected": {},
                "modismos_detallados": [],
                "total_modismos": 0,
                "status": "error",
                "beto_available": False,
                "phi_available": False,
            }

    @staticmethod
    def analyze_audio(file_bytes: bytes, filename: str, content_type: str):
        """
        Analiza un archivo de audio: transcribe con Whisper y luego analiza con BETO + PHI.
        """
        if not content_type:
            content_type = "audio/wav"  # fallback seguro

        whisper_url = f"{settings.WHISPER_URL}/transcribe"
        files = {"file": (filename, file_bytes, content_type)}

        # Llamar a Whisper
        response = requests.post(whisper_url, files=files, timeout=60)
        if response.status_code != 200:
            raise Exception(f"Error al transcribir audio: {response.text}")

        whisper = response.json()
        text = whisper.get("transcription", "")

        # Analizar el texto resultante
        return OrchestratorService.analyze_text(text)
