from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.settings import postgre_settings


DATABASE_URL = (f"postgresql+asyncpg://"
                f"{postgre_settings.DB_USER}:"
                f"{postgre_settings.DB_PASS}@"
                f"{postgre_settings.DB_HOST}:"
                f"{postgre_settings.DB_PORT}/"
                f"{postgre_settings.DB_NAME}")

engine = create_async_engine(DATABASE_URL)
AsyncSessionMaker = async_sessionmaker(bind=engine)