from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    title: str = "MAPOINTS"
    description: str = "The API for building a map of the points and finding the best way."
    version: str = "0.1.1"
    debug: bool = Field(False, env="DEBUG")
    
    API_PREFIX: str = "/api"
    
    class Config:
        env_file = ".env"
        

settings = Settings()
