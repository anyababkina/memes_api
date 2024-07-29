from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers.s3_routers import router
from src.settings import env_settings, s3_settings
from src.helpers import S3FileManager


@asynccontextmanager
async def lifespan(app_memes: FastAPI):
    S3FileManager.create_bucket(s3_settings.BUCKET_NAME)
    yield


app = FastAPI(
    title="API S3 Service",
    description="Documentation for api s3 service",
    version="0.0.1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS", "PUT", "POST", "DELETE", "PATCH"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host=str(env_settings.S3_API_HOST), port=int(env_settings.S3_API_PORT))