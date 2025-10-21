from pydantic import BaseModel
from typing import List

class Creatreceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str
    
class receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str