from http import HTTPStatus
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List, Dict
from schema import Creatreceita,receita, usuario, UsuarioCreate, UsuarioPublic, UsuarioUpdate


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
def criar_usuario(usuario_data: UsuarioCreate):
    global proximo_id_usuario

    for user in usuarios_db.values():
        if user.email == usuario_data.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Já existe um usuario com esse email."
            )
        
    novo_usuario = usuario (
            id=proximo_id_usuario,
            username=usuario_data.username,
            email=usuario_data.email,
            password=usuario_data.password
    )

    usuarios_db[proximo_id_usuario] = novo_usuario
    proximo_id_usuario += 1

    return novo_usuario


@app.get("/usuarios", response_model=List[UsuarioPublic])
def listar_usuarios():
    return list(usuarios_db.values())

# Rota GET (Usuário por ID)
@app.get("/usuarios/id/{user_id}", response_model=UsuarioPublic)
def buscar_usuario_por_id(user_id: int):
    if user_id not in usuarios_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado."
        )
    return usuarios_db[user_id]

@app.get("/usuarios/nome/{username}", response_model=UsuarioPublic)
def buscar_usuario_por_nome(username: str):
    for user in usuarios_db.values():
        if user.username.lower() == username.lower():
            return user
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Usuário não encontrado."
    )

@app.put("/usuarios/{user_id}", response_model=UsuarioPublic)
def editar_usuario(user_id: int, usuario_data: UsuarioUpdate):
    if user_id not in usuarios_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    usuario_existente = usuarios_db[user_id]
    
    update_data = usuario_data.model_dump(exclude_unset=True)

    if 'email' in update_data and update_data['email'] != usuario_existente.email:
        for user in usuarios_db.values():
            if user.email == update_data['email'] and user.id != user_id:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Já existe outro usuário com este email."
                )

    updated_user = usuario_existente.model_copy(update=update_data)
    
    usuarios_db[user_id] = updated_user
    
    return updated_user

@app.delete("/usuarios/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_usuario(user_id: int):
    if user_id not in usuarios_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    del usuarios_db[user_id]
    return