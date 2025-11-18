from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator 
from settings import Settings

settings = Settings()

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoFlush=False, bind=engine)

def get_session() ->Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()