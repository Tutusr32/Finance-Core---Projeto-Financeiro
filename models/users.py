from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column("nome", String(100), nullable=False)
    email = Column(String(100), nullable=False)

    contas = relationship(
        "Contas",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
    