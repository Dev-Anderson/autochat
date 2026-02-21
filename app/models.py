from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


# 🏢 Empresa
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # relacionamento com usuários
    users = relationship("User", back_populates="company", cascade="all, delete")


# 👤 Usuário (admin geral ou admin da empresa)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # papel do usuário (super_admin ou company_admin)
    role = Column(String, default="company_admin", nullable=False)

    # pode ser nulo para super_admin
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)

    # relacionamento com empresa
    company = relationship("Company", back_populates="users")