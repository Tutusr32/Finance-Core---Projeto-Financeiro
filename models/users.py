from sqlalchemy import Column, String, Integer
from configs.base import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    contas = relationship("Contas", back_populates="user")

    def __repr__(self):
        return f"| ID:{self.id} | {self.nome} | {self.email} |"
