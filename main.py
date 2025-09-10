from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class Receita(BaseModel):
   nome: str
   ingredientes: List[str]
   modo_de_preparo: str

app = FastAPI()

receitas = [
    {
        "nome": "brownie",
        "ingredientes": ["3 ovos", "6 colheres de açúcar", "200g de chocolate", "100g de manteiga"],
        "utensílios": ["tigela", "forma", "forno"],
        "modo_preparo": "Misture tudo, leve ao forno a 180°C por 30 minutos."
    },
    {
        "nome": "torta",
        "ingredientes": ["3 ovos", "2 xícaras de farinha", "1 xícara de leite", "1/2 xícara de óleo"],
        "utensílios": ["tigela", "forma", "forno"],
        "modo_preparo": "Misture os ingredientes, despeje na forma e asse a 200°C por 40 minutos."
    },
    {
        "nome": "bolo de cenoura",
        "ingredientes": ["3 cenouras", "3 ovos", "2 xícaras de farinha", "1 xícara de açúcar"],
        "utensílios": ["liquidificador", "forma", "forno"],
        "modo_preparo": "Bata as cenouras com ovos, adicione os secos e asse por 40 minutos."
    },
    {
        "nome": "pudim",
        "ingredientes": ["1 lata de leite condensado", "2 latas de leite", "3 ovos"],
        "utensílios": ["liquidificador", "forma de pudim", "forno"],
        "modo_preparo": "Bata tudo, caramelize a forma e asse em banho-maria por 1 hora."
    },
    {
        "nome": "panqueca",
        "ingredientes": ["2 ovos", "1 xícara de leite", "1 xícara de farinha", "sal a gosto"],
        "utensílios": ["tigela", "frigideira"],
        "modo_preparo": "Bata os ingredientes e frite pequenas porções na frigideira."
    },
    {
        "nome": "pizza caseira",
        "ingredientes": ["2 xícaras de farinha", "1 ovo", "1/2 xícara de leite", "queijo", "molho de tomate"],
        "utensílios": ["tigela", "forma", "forno"],
        "modo_preparo": "Prepare a massa, adicione o recheio e leve ao forno a 220°C por 20 minutos."
    }
]

@app.get("/")
def hello():
    return {"title": "Livro de Receitas"}


@app.get("/receita")
def listar_receitas():
    return receitas


@app.get("/receita/{nome}")
def get_receita_por_nome(nome_receita: str):
    for r in receitas:
        if receita.nome == nome_receita:
            return receita
        
    return {"erro": "Receita não encontrada"}

@app.post("/receitas")
def create_receita(dados: Receita):
    nova_receita = dados,dict()

    receita.append(nova_receita)

    return nova_receita