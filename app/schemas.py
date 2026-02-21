from pydantic import BaseModel, EmailStr


# 👤 criação de usuário
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# 🔐 login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# 🏢 criação de empresa + usuário admin
class CompanyCreate(BaseModel):
    company_name: str
    user_name: str
    email: EmailStr
    password: str


# 📤 resposta de usuário (sem senha)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    company_id: int | None

    class Config:
        from_attributes = True  # permite converter de ORM (SQLAlchemy)


# 📤 resposta de empresa
class CompanyResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True