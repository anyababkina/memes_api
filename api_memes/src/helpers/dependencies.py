from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database import AsyncSessionMaker


async def get_session_maker() -> async_sessionmaker:
    yield AsyncSessionMaker


AsyncSessionMakerDep = Annotated[async_sessionmaker, Depends(get_session_maker)]