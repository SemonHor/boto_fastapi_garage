from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        env_file='.env'
    )
    BASE_ROUTE_PATH: str = '/api/v1'
    
    S3_BUCKET_NAME: str = ''
    S3_URL: str = ''
    S3_KEY_ID: str = ''
    S3_SECRET_KEY: str = ''
    S3_REGION: str = ''


settings = Settings()

APP_VERSION = '0.1.0'
