from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Enum, DateTime, func
from configs.base import Base

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
        return f"| ID:{self.id} | {self.conta_id} | {self.tipo} | {self.valor} | {self.categoria} | {self.data} |"
