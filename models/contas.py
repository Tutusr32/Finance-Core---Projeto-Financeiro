from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from core.base import Base


class Contas(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column("nome", String(100), nullable=False)
    saldo = Column(Numeric(10, 2), nullable=False)

    user = relationship("Users", back_populates="contas")
    transacoes = relationship("Transacoes", back_populates="conta")

    def __repr__(self):
        return f"<Conta(id={self.id}, user_id={self.user_id}, name='{self.name}', saldo={self.saldo})>"
    