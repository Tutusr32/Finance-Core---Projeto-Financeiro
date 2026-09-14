from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from core.base import Base


class OcorrenciasRecorrentes(Base):
    __tablename__ = "ocorrencias_recorrentes"

    id = Column(Integer, primary_key=True)
    transacao_recorrente_id = Column(
        Integer, ForeignKey("transacoes_recorrentes.id"), nullable=False
    )
    transacao_id = Column(Integer, ForeignKey("transacoes.id"), nullable=True)

    data_prevista = Column(Date, nullable=False)
    data_processamento = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum("pendente", "realizada", "falhou"), nullable=False, default="pendente")
    motivo_falha = Column(String(255), nullable=True)

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

    transacao_recorrente = relationship(
        "TransacoesRecorrentes",
        back_populates="ocorrencias",
    )

    transacao = relationship(
        "Transacoes",
        back_populates="ocorrencia_recorrente",
    )
