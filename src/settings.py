"""
settings
"""
from typing import Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    model settings
    """
    token: str
    db_user: str
    db_password: str
    external_db_port: str
    db_port: str
    db_container_name: str
    bot_port: int
    base_url: str
    overdue_time_sleep: Union[int | float]
    queue_time_sleep: Union[int | float]
    is_overdue_time: int


settings = Settings()  # type: ignore
