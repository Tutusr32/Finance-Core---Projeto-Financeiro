def transacao_to_dict(transacao):
    return {
        "id": transacao.id,
        "conta_id": transacao.conta_id,
        "type": transacao.tipo,
        "amount": float(transacao.valor),
        "category": transacao.categoria,
        "data": transacao.data.isoformat() if transacao.data else None,
    }
