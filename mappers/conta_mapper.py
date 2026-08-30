def conta_to_dict(conta):
    return {
        "id": conta.id,
        "user_id": conta.user_id,
        "user_name": conta.user.name,
        "name": conta.name,
        "saldo": str(conta.saldo),
        "created_at": conta.created_at.isoformat(),
        "updated_at": conta.updated_at.isoformat(),
    }
