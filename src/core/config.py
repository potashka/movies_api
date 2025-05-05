# src/core/config.py сокорректирован по итогам review
import os
from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from .logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):                           # добавлено
    """
    Конфигурация приложения. Переменные читаются из `.env`
    и валидируются pydantic‑ом.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # --- приложение ---
    project_name: str = Field("movies-api", alias="PROJECT_NAME")    # изменено

    # --- Redis ---
    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")

    # --- Elasticsearch ---
    elastic_schema: str = Field("http://", alias="ELASTIC_SCHEMA")
    elastic_host: str = Field("127.0.0.1", alias="ELASTIC_HOST")
    elastic_port: int = Field(9200, alias="ELASTIC_PORT")

    # --- Postgres ---
    pg_host: str = Field("127.0.0.1", alias="PG_HOST")
    pg_port: int = Field(5432, alias="PG_PORT")
    pg_db: str = Field("movies_db", alias="PG_DB")
    pg_user: str = Field("app", alias="PG_USER")
    pg_password: str = Field("secret", alias="PG_PASSWORD")

    # --- режим «только документация» ---
    docs_only: bool = Field(False, alias="DOCS_ONLY")


# добавлено
settings = Settings()
