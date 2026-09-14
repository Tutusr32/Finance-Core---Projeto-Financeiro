from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from core.base import Base


class TransacoesRecorrentes(Base):
    __tablename__ = "transacoes_recorrentes"

    id = Column(Integer, primary_key=True)
    conta_id = Column(Integer, ForeignKey("contas.id"), nullable=False)
    tipo = Column(Enum("entrada", "saida"), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(50), nullable=False)

    frequencia = Column(Enum("semanal", "quinzenal", "mensal"), nullable=False)
    data_inicio = Column(Date, nullable=False)
    proxima_data = Column(Date, nullable=False)

    ativo = Column(Boolean, nullable=False, default=True)

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

    conta = relationship(
        "Contas",
        back_populates="transacoes_recorrentes",
    )

    ocorrencias = relationship(
        "OcorrenciasRecorrentes",
        back_populates="transacao_recorrente",
        cascade="all, delete-orphan",
    )
