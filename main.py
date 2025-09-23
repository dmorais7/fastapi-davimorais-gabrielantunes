from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    utensilios: List[str]
    modo_preparo: str


receitas: List[Receita] = [
    Receita(
        nome="brownie",
        ingredientes=["3 ovos", "6 colheres de açúcar", "200g de chocolate", "100g de manteiga"],
        utensilios=["tigela", "forma", "forno"],
        modo_preparo="Misture tudo, leve ao forno a 180°C por 30 minutos."
    ),
    Receita(
        nome="torta",
        ingredientes=["3 ovos", "2 xícaras de farinha", "1 xícara de leite", "1/2 xícara de óleo"],
        utensilios=["tigela", "forma", "forno"],
        modo_preparo="Misture os ingredientes, despeje na forma e asse a 200°C por 40 minutos."
    ),
    Receita(
        nome="bolo de cenoura",
        ingredientes=["3 cenouras", "3 ovos", "2 xícaras de farinha", "1 xícara de açúcar"],
        utensilios=["liquidificador", "forma", "forno"],
        modo_preparo="Bata as cenouras com ovos, adicione os secos e asse por 40 minutos."
    ),
    Receita(
        nome="pudim",
        ingredientes=["1 lata de leite condensado", "2 latas de leite", "3 ovos"],
        utensilios=["liquidificador", "forma de pudim", "forno"],
        modo_preparo="Bata tudo, caramelize a forma e asse em banho-maria por 1 hora."
    ),
    Receita(
        nome="panqueca",
        ingredientes=["2 ovos", "1 xícara de leite", "1 xícara de farinha", "sal a gosto"],
        utensilios=["tigela", "frigideira"],
        modo_preparo="Bata os ingredientes e frite pequenas porções na frigideira."
    ),
    Receita(
        nome="pizza caseira",
        ingredientes=["2 xícaras de farinha", "1 ovo", "1/2 xícara de leite", "queijo", "molho de tomate"],
        utensilios=["tigela", "forma", "forno"],
        modo_preparo="Prepare a massa, adicione o recheio e leve ao forno a 220°C por 20 minutos."
    )
]


@app.get("/")
def hello():
    return {"title": "Livro de Receitas"}


@app.get("/Receita")
def listar_Receita():
    return Receita



@app.get("/Receitas/{nome_receita}")
def get_receita_por_nome(nome_receita: str):
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():
            return receita
    return {"erro": "Receita não encontrada"}


@app.post("/Receitas")
def create_Receita(dados: Receita):
    receitas.append(dados)
    return dados

@app.put("/Receita/{id}")
def update_Receita(id:int, dados:Receita):
    for i in range(len(receitas)):
        if receitas[i]. id==id:  
            receita_atualizada = Receita(
                id=id,
                nome=dados.nome,
                ingredientes=dados.ingredientes,
                 modo_preparo=dados.modo_preparo,
            )      
            receitas[i] = (receita_atualizada) 
            return receita_atualizada
  
        return {"mensagem": "receita não encontrada"} 