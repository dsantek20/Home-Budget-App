import logging
from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from pydantic.v1 import BaseSettings

log = logging.getLogger(__name__)


class AppConfiguration(BaseSettings):
    app_name: str = "Home Budget"
    debug: bool = False
    log_file_path: str
    log_file_name: str
    database_url: str
    alembic_database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expiration_hours: int
    test_database_url: str

    class Config:
        file = f".env"
        log.info("Config file used: " + file)
        env_file = file


@lru_cache
def get_app_config() -> AppConfiguration:
    return AppConfiguration()

AppConfig = Annotated[AppConfiguration, Depends(get_app_config)]