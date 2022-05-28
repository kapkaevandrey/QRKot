from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Cat donation'
    description: str = 'QRKot Cat Support Charity Foundation'
    database_url: str
    secret: str = 'Where`s my fucking milk'

    class Config:
        env_file = '.env'


settings = Settings()
