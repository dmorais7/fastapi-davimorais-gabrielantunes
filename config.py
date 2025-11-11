from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    datbase_url: str = 'sqlite:///>/db.sqlite3'

settings = Settings()