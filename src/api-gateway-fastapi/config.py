from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CATALOGO_URL: str
    LOGISTICA_URL: str
    GATEWAY_URL: str
    RABBITMQ_URL: str
    #database_url: str = "sqlite:///./test.db" # Valor padrão
    debug: bool = False

    class Config:
        env_file = ".env" 

settings = Settings()