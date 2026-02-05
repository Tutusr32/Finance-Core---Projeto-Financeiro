from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from configs.base import Base

class Contas(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nome = Column(String(100), nullable=False)
    saldo = Column(Numeric(10, 2), nullable=False)

    user = relationship("Users", back_populates="contas")
    transacoes = relationship("Transacoes", back_populates="conta")

    def __repr__(self):
        return f"| ID:{self.id} | {self.user.nome} | {self.nome} | {self.saldo} |"
