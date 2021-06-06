from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_password: str

    class Config:
        env_file = "../.env"

settings = Settings()