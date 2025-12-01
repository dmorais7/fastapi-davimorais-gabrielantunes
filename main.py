from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict
from schema import Creatreceita,receita, usuario, UsuarioCreate, UsuarioPublic, UsuarioUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User 
from database import get_session

receitas: List[receita] = []
proximo_id_receita = 1

app = FastAPI()

id: int
nome: str
ingredientes: List[str]
modo_de_preparo: str

nome: str
ingredientes: List[str]
modo_de_preparo: str
receitas: List[receita] = []
proximo_id_receita = 1

usuarios_db: Dict[int, usuario] = {}
proximo_id_usuario = 1
proximo_id_receita = 1

@app.get("/")
def hello():
    return {"title": "Livro de Receitas"}


@app.get("/receita")
def listar_receitas():
    return receitas

@app.get("/receitas/id/{id}")
def buscar_receita(id: int):
    for r in receitas: 
        if r.id == id:
            return r
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.get("/receitas/nome/{nome}", response_model=receita, status_code=HTTPStatus.OK)
def buscar_receita_por_nome(nome: str):
    for r in receitas:
        if r.nome.lower() == nome.lower():
            return r
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

@app.post("/receitas")
def criar_receita(dados: Creatreceita):
    global proximo_id

    for r in receitas:
        if r.nome.lower() == dados.nome.lower():
            raise HTTPException(status_code=400, detail="Receita já existente.")
    nova_receita =receita(id = proximo_id , nome = dados.nome, ingredientes = dados.ingredientes, modo_de_preparo = dados.modo_de_preparo)
    receitas.append(nova_receita)
    proximo_id += 1
    return nova_receita

@app.put("/receitas/{id}", response_model=receita)
def update_receita(id: int, dados: Creatreceita):
    for r in receitas:
        if r.id != id and r.nome.lower() == dados.nome.lower():
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe receita com esse nome")
    
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_atualizada = receita(
                id= id,
                nome= dados.nome,
                ingredientes = dados.ingredientes,
                modo_de_preparo = dados.modo_de_preparo,
            )
            receitas[i] = receita_atualizada
            return receita_atualizada
    raise HTTPException(status_code=404, detail="Erro!Receita não encontrada")

@app.delete("/receitas/{id}")
def deletar_receita(id: int):
    if not receitas:
       return {"mensagem": "Não há receitas para excluir."}
     
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receitas.pop(i)
            return {"mensagem": "Receita deletada"}
    return {"mensagem": "Erro!Receita não encontrada"}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Erro!Receita não encontrada")

@app.post("/usuarios", response_model=UsuarioPublic, status_code=HTTPStatus.CREATED)
def criar_usuario(
    usuario_data: UsuarioCreate,
    session: Session = Depends(get_session)
    ):

    user_by_email = session.scalar(
        select(User).where(User.email == usuario_data.email)
    )
    user_by_username = session.scalar(
        select(User).where(User.username == usuario_data.username)
    )

 
    if user_by_email == usuario_data.email:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Já existe um usuario com esse email."
        )
        
    novo_usuario = User(
            id=proximo_id_usuario,
            username=usuario_data.username,
            email=usuario_data.email,
            password=usuario_data.password
    )

    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return novo_usuario


@app.get("/usuarios", response_model=List[UsuarioPublic])
def listar_usuarios (Session: Session: Depends(get_session, skip: int = 0, limit: int = 100)):

usuarios = Session.scalars(
    select(User)
    .offset(skip)
    .limit(limit)
).all()

return listar_usuarios

@app.get("/usuarios/id/{user_id}", response_model=UsuarioPublic)
def buscar_usuario_por_id(user_id: int, session: Session =  Depends(get_session)):

    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado."
        )
    return db_user

@app.get("/usuarios/nome/{username}", response_model=UsuarioPublic)
def buscar_usuario_por_nome(username: str, session: Session = Depends(get_session)):

    db_user +session.scalar(select(User).where(User.username == username))
   
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado."
    )

    return db_user

@app.put("/usuarios/{user_id}", response_model=UsuarioPublic)
def editar_usuario(user_id: int, usuario_data: UsuarioUpdate, session: Session = Depends(get_session)):
    
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    usuario_existente = usuarios_db[user_id]
    
    update_data = usuario_data.model_dump(exclude_unset=True)

    if 'email' in update_data and update_data['email'] != usuario_existente.email:
        user_by_email = session.scalar(
            select(User).where(User.email == update_data["email"])
        )

    if user_by_email:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Email já existe para outro usuário.",
        )

    if "username" in update_data and update_data["username"] != db_user.username:
        user_by_username = session.scalar(
            select(User).where(User.username == update_data["username"])
        )
        if user_by_username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Nome de usuário já existe para outro usuário.",
            )
        
    for key, value in update_data.items():
        setattr(db_user, key, value)
    updated_user = usuario_existente.model_copy(update=update_data)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.delete("/usuarios/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_usuario(user_id: int, session: Sessions = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    session.delete(db_user)
    session.commit()
    
    return None