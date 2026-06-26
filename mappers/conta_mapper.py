from schemas.contas import ContaSchema

def conta_to_dict(conta):
    return {
        "id": conta.id,
        "user_id": conta.user_id,
        "nome_usuario": conta.user.nome,
        "nome": conta.nome,
        "saldo": str(conta.saldo)
    }
