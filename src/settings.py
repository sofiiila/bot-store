from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str
    db_user: str
    db_password: str
    external_db_port: str = '27017'
    db_port: str = '27017'

    class Config:
        env_file = '.env'


settings = Settings()
