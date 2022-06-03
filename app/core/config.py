from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Пожертвования для котиков'
    app_description: str = 'QRKot поддержка проектов для котиков'
    database_url: str = 'sqlite+aiosqlite:///./charity_cat_foundation.db'
    secret: str = 'Верните моё молоко'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
