import os
from logging import config as logging_config

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies-api')

# Redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Elasticsearch
ELASTIC_SCHEMA = os.getenv('ELASTIC_SCHEMA', 'http://')
ELASTIC_HOST   = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT   = int(os.getenv('ELASTIC_PORT', 9200))

# Postgres (для тестов/ETL)
PG_HOST     = os.getenv('PG_HOST', '127.0.0.1')
PG_PORT     = int(os.getenv('PG_PORT', 5432))
PG_DB       = os.getenv('PG_DB', 'movies_db')
PG_USER     = os.getenv('PG_USER', 'app')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'secret')

# Режим без внешних сервисов (по умолчанию False)
DOCS_ONLY = os.getenv("DOCS_ONLY", "false").lower() == "true"