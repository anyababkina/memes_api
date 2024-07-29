import os

from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    S3_API_HOST: str = os.environ.get("S3_API_HOST", 'localhost')
    S3_API_PORT: str = os.environ.get("S3_API_PORT", '8000')


class S3Settings(BaseSettings):
    ENDPOINT_URL: str = os.environ.get('ENDPOINT_URL', '')
    ACCESS_KEY: str = os.environ.get("ACCESS_KEY", '')
    SECRET_ACCESS_KEY: str = os.environ.get("SECRET_ACCESS_KEY", '')
    BUCKET_NAME: str = os.environ.get("BUCKET_NAME", '')


env_settings = EnvSettings()
s3_settings = S3Settings()