import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "Climate Debate Analyzer"
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    nasa_api_key: str = os.getenv("NASA_API_KEY")
    database_url: str = "sqlite:///./climate.db"
    
    class Config:
        env_file = ".env"

settings = Settings()