import multiprocessing as mp

from loguru import logger
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()


class Postgres(BaseModel):
    database: str = os.getenv("POSTGRES_DB")
    host: str = os.getenv("HOST_POSTGRES")
    port: int = int(os.getenv("PORT_POSTGRES"))
    username: str = os.getenv("POSTGRES_USER")
    password: str = os.getenv("POSTGRES_PASSWORD")
    url: str = os.getenv("POSTGRES_URL")


class Uvicorn(BaseModel):
    host: str = os.getenv("HOST_BACKEND")
    port: int = int(os.getenv("PORT_BACKEND"))
    workers: int = mp.cpu_count() * 2 + 1


class _Settings(BaseSettings):
    pg: Postgres = Postgres()
    uvicorn: Uvicorn = Uvicorn()

    #model_config = SettingsConfigDict(env_file=".env", env_prefix="app_", env_nested_delimiter="__")


settings = _Settings()
logger.info("settings.inited {}", settings.model_dump_json())
