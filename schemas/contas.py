from dataclasses import dataclass
from decimal import Decimal

@dataclass
class ContaSchema:
    id: int
    user_id: int
    nome_usuario: str
    nome: str
    saldo: Decimal