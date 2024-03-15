from fastapi import FastAPI, HTTPException

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
                validar_saldo_negativo(valor, conta)
                conta["valor_na_conta"] -= valor
            else:
                raise HTTPException(status_code=400, detail="Tipo inválido")
            conta["transacoes"].append({
                "valor": valor,
                "tipo": tipo,
                "descricao": descricao
            })
            return conta
    raise HTTPException(status_code=404, detail="Conta inexistente")


@app.get("/clientes/[id]/transacoes")
async def ler_transacoes(id: int):
    for conta in contasBanco:
        if conta["id"] == id:
            return conta["transacoes"]
    raise HTTPException(status_code=404, detail="Conta inexistente")


@app.get("/clientes/[id]/transacoes/[transacao_id]")
async def ler_transacao(id: int, transacao_id: int):
    for conta in contasBanco:
        if conta["id"] == id:
            for i in range(len(conta["transacoes"])):
                if i == transacao_id:
                    return conta["transacoes"][transacao_id]
            raise HTTPException(status_code=404, detail="Transação inexistente")
    raise HTTPException(status_code=404, detail="Conta inexistente")


@app.put("/clientes/[id]/transacoes/[transacao_id]")
async def atualizar_transacao(id: int, transacao_id: int, valor: float, tipo: str, descricao: str):
    for conta in contasBanco:
        if conta["id"] == id:
            if transacao_id >= len(conta["transacoes"]):
                raise HTTPException(status_code=404, detail="Transação inexistente")
            for i in range(len(conta["transacoes"])):
                if i == transacao_id:
                    transacao = conta["transacoes"][transacao_id]
                    if tipo != "c" and tipo != "d":
                        raise HTTPException(status_code=400, detail="Tipo inválido")
                    elif transacao["tipo"] == "c" and tipo == "d":
                        if conta["valor_na_conta"] < transacao["valor"] + valor:
                            raise HTTPException(status_code=400, detail="Saldo insuficiente")
                        conta["valor_na_conta"] -= transacao["valor"] + valor
                    elif transacao["tipo"] == "d" and tipo == "c":
                        if conta["valor_na_conta"] < transacao["valor"] + valor:
                            raise HTTPException(status_code=400, detail="Saldo insuficiente")
                        conta["valor_na_conta"] += transacao["valor"] + valor
                    else:
                        valor_conta = conta["valor_na_conta"]
                        if transacao["tipo"] == "c":
                            if (valor_conta - transacao["valor"]) + valor < 0:
                                raise HTTPException(status_code=400, detail="Saldo insuficiente")
                            conta["valor_na_conta"] -= transacao["valor"]
                            conta["valor_na_conta"] += valor
                        else:
                            if (valor_conta + transacao["valor"]) - valor < 0:
                                raise HTTPException(status_code=400, detail="Saldo insuficiente")
                            conta["valor_na_conta"] += transacao["valor"]
                            conta["valor_na_conta"] -= valor
                    conta["transacoes"][i] = {
                        "valor": valor,
                        "tipo": tipo,
                        "descricao": descricao
                    }
                return conta["transacoes"][i]


@app.delete("/clientes/[id]/transacoes/[transacao_id]", status_code=204)
async def deletar_transacao(id: int, transacao_id: int):
    for conta in contasBanco:
        if conta["id"] == id:
            for i in range(len(conta["transacoes"])):
                if i == transacao_id:
                    transacao = conta["transacoes"][transacao_id]
                    if transacao["tipo"] == "c":
                        conta["valor_na_conta"] -= transacao["valor"]
                    else:
                        conta["valor_na_conta"] += transacao["valor"]
                    conta["transacoes"].pop(transacao_id)
                    return None
            raise HTTPException(status_code=404, detail="Transação inexistente")
    raise HTTPException(status_code=404, detail="Conta inexistente")


@app.get("/clientes/[id]")
async def ler_cliente(id: int):
    for conta in contasBanco:
        if conta["id"] == id:
            return conta
    raise HTTPException(status_code=404, detail="Conta inexistente")
