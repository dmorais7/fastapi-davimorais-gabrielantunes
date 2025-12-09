from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator 
from settings import Settings

settings = Settings()

engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoFlush=False, bind=engine)

def get_session() ->Generator[Session, None ,None]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()