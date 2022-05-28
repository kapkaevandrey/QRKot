from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv('.env')


class Settings(BaseSettings):
    app_title: str = 'Cat donation'
    description: str = 'QRKot Cat Support Charity Foundation'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'Where`s my fucking milk'

    class Config:
        env_file = '.env'


settings = Settings()
