from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import user, table_registry

app = FastAPI(title='API de teste')

engine = create_engine("sqlite:///:memory:", echo=True)

table_registry.metadata.create_all(engine)


with Session(engine) as session:
    print(" Criando utilizador")
    mairon = user(
        username="mairon", password="senha123", email="mairon@email.com"
    )

    session.add(mairon)
    session.commit()  
    session.refresh(mairon) 
     
    print(mairon)
