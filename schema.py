from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class Creatreceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str
    
class receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str
    user_id: int

class BaseUsuario(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UsuarioCreate(BaseUsuario):
    password: str = Field(..., min_length=6)

class UsuarioUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)

class UsuarioPublic(BaseUsuario):
    id: int
    
    class Config:
        from_attributes = True

class Usuario(UsuarioPublic):
    id: int
    
    class Config:
        from_attributes = True