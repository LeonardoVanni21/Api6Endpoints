from fastapi import FastAPI

app = FastAPI()

contasBanco = [
    {
        "id": 1,
        "nome": "Silvio Santos",
        "valor_na_conta": 10000,
        "transacoes": [
            {
                "valor": 1500,
                "tipo": "d",
                "descricao": "Uma transacao"
            }
        ],
    },
    {
        "id": 2,
        "nome": "Fausto Silva",
        "valor_na_conta": 10,
        "transacoes": [
            {
                "valor": 1500,
                "tipo": "c",
                "descricao": "Uma transacao"
            },
            {
                "valor": 32,
                "tipo": "d",
                "descricao": "Uma transacao"
            }
        ],
    },
    {
        "id": 3,
        "nome": "Gugu liberato",
        "transacoes": [],
    }
]


@app.post("/clientes/[id]/transacoes")
async def criar_transacao(id: int, valor: float, tipo: str, descricao: str):
    for conta in contasBanco:
        if conta["id"] == id:
            if tipo == "c":
                conta["valor_na_conta"] += valor
            elif tipo == "d":
                if valor > conta["valor_na_conta"]:
                    return {"error": "Saldo insuficiente"}
                conta["valor_na_conta"] -= valor
            else:
                return {"error": "Tipo inválido"}
            conta["transacoes"].append({
                "valor": valor,
                "tipo": tipo,
                "descricao": descricao
            })
            return conta
    return {"error": "Conta inexistente"}


@app.get("/clientes/[id]/transacoes")
async def ler_transacoes(id: int):
    for conta in contasBanco:
        if conta["id"] == id:
            return conta["transacoes"]
    return {"error": "Conta inexistente"}
