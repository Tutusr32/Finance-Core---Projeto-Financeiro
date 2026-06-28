from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from core.base import Base


class Transacoes(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True)
    conta_id = Column(Integer, ForeignKey("contas.id"), nullable=False)
    tipo = Column(Enum("entrada", "saida"), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(50), nullable=False)
    data = Column(DateTime, server_default=func.now())

    conta = relationship("Contas", back_populates="transacoes")

    def __repr__(self):
        return (
            f"| ID:{self.id} | "
            f"{self.conta_id} | "
            f"{self.tipo} | "
            f"{self.valor} | "
            f"{self.categoria} | "
            f"{self.data} |"
        )
