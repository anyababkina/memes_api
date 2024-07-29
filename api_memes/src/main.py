import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers.memes import router
from src.settings import env_settings

app = FastAPI(
    title="API Memes Service",
    description="Documentation for api memes service",
    version="0.0.1",
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
    uvicorn.run(app, host=str(env_settings.API_MEMES_HOST), port=int(env_settings.API_MEMES_PORT))