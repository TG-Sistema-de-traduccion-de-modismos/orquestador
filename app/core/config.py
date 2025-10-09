from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WHISPER_URL: str = "http://100.109.110.59:8002"
    BETO_URL: str = "http://100.109.110.59:8003"
    PHI_URL: str = "http://100.109.110.59:8004"
    VERSION: str = "2.0"

    class Config:
        env_file = ".env"

settings = Settings()
