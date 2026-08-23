from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from core.base import Base


class Contas(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column("nome", String(100), nullable=False)
    saldo = Column(Numeric(10, 2), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("Users", back_populates="contas")
    transacoes = relationship(
        "Transacoes",
        back_populates="conta",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<Conta(id={self.id}, user_id={self.user_id}, name='{self.name}', saldo={self.saldo})>"
        )
