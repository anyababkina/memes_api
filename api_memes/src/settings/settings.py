import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class PostgreSettings(BaseSettings):
    DB_HOST: str = os.environ.get("DB_HOST", '')
    DB_PORT: str = os.environ.get("DB_PORT", '')
    DB_NAME: str = os.environ.get("DB_NAME", '')
    DB_USER: str = os.environ.get("DB_USER", '')
    DB_PASS: str = os.environ.get("DB_PASS", '')


class EnvSettings(BaseSettings):
    API_MEMES_HOST: str = os.environ.get("API_MEMES_HOST", 'localhost')
    API_MEMES_PORT: str = os.environ.get("API_MEMES_PORT", '8000')
    S3_API_HOST: str = os.environ.get("S3_API_HOST", 'localhost')
    S3_API_PORT: str = os.environ.get('S3_API_PORT', '8001')


class TestSettings(BaseSettings):
    TEST_POSTGRES_IMAGE: str = "postgres:14"
    TEST_POSTGRES_USER: str = "postgres"
    TEST_POSTGRES_PASSWORD: str = "test_password"
    TEST_POSTGRES_DATABASE: str = "test_database"
    TEST_POSTGRES_CONTAINER_PORT: int = 5432


postgre_settings = PostgreSettings()
env_settings = EnvSettings()
test_settings = TestSettings()