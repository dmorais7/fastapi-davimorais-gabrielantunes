from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_preparo: str

class Creatreceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_preparo: str
receitas: List[receita] = []
proximo_id = 1


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


