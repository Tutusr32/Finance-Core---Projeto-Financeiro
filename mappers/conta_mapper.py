def conta_to_dict(conta):
    return {
        "id": conta.id,
        "user_id": conta.user_id,
        "user_name": conta.user.name,
        "name": conta.name,
        "saldo": str(conta.saldo),
    }
