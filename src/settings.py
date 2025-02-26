"""
settings
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    model settings
    """
    token: str
    db_user: str
    db_password: str
    # TODO данная переменная не нужна
    external_db_port: str
    db_port: str
    db_container_name: str
    bot_port: int
    base_url: str
    overdue_time_sleep: int
    queue_time_sleep: int
    is_overdue_time: int = 10
    tmp_dir: str


settings = Settings()  # type: ignore
