from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User, Receita as ReceitaORM 
from schema import CreateReceita, Receita, Usuario, UsuarioCreate, UsuarioUpdate 
from database import get_session

app = FastAPI()


@app.get("/receitas", response_model=List[Receita])
def listar_receitas(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0, le=100)
):
   
    receitas_db = session.scalars(
        select(ReceitaORM).offset(skip).limit(limit)
    ).all()
    
   
    return receitas_db

@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.CREATED)
def criar_receita(receita: CreateReceita, session: Session = Depends(get_session)):
    
    
    nova_receita_db = ReceitaORM(user_id=1, **receita.model_dump())
    session.add(nova_receita_db)
    session.commit()
    session.refresh(nova_receita_db)
    return nova_receita_db

@app.get("/receitas/{receita_id}", response_model=Receita)
def buscar_receita(receita_id: int, session: Session = Depends(get_session)):
    receita_db = session.get(ReceitaORM, receita_id)
    if not receita_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")
    return receita_db

@app.put("/receitas/{receita_id}", response_model=Receita)
def atualizar_receita(receita_id: int, receita_atualizada: CreateReceita, session: Session = Depends(get_session)):
    receita_db = session.get(ReceitaORM, receita_id)
    if not receita_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

    for key, value in receita_atualizada.model_dump().items():
        setattr(receita_db, key, value)
    
    session.commit()
    session.refresh(receita_db)
    return receita_db

@app.delete("/receitas/{receita_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_receita(receita_id: int, session: Session = Depends(get_session)):
    receita_db = session.get(ReceitaORM, receita_id)
    if not receita_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")
    
    session.delete(receita_db)
    session.commit()
    return

# --- Rotas de Usuários ---

@app.post("/usuarios", response_model=Usuario, status_code=HTTPStatus.CREATED)
def criar_usuario(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    # Criação do hash da senha (necessário para um código "zero bala")
    # OBS: Você precisará instalar uma biblioteca de hash de senha, como 'passlib'
    # Exemplo: hashed_password = pwd_context.hash(usuario.password)
    
    # Por enquanto, vamos usar a senha em texto puro (NÃO RECOMENDADO EM PRODUÇÃO)
    novo_usuario_db = User(**usuario.model_dump())
    
    session.add(novo_usuario_db)
    session.commit()
    session.refresh(novo_usuario_db)
    return novo_usuario_db

@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0, le=100)
):
    usuarios_db = session.scalars(
        select(User).offset(skip).limit(limit)
    ).all()
    return usuarios_db

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def buscar_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario_db = session.get(User, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    return usuario_db

@app.put("/usuarios/{usuario_id}", response_model=Usuario)
def atualizar_usuario(usuario_id: int, usuario_atualizado: UsuarioUpdate, session: Session = Depends(get_session)):
    usuario_db = session.get(User, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    update_data = usuario_atualizado.model_dump(exclude_unset=True)
    
    # Atualiza apenas os campos fornecidos
    for key, value in update_data.items():
        setattr(usuario_db, key, value)
    
    session.commit()
    session.refresh(usuario_db)
    return usuario_db

@app.delete("/usuarios/{usuario_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario_db = session.get(User, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    
    session.delete(usuario_db)
    session.commit()
    return