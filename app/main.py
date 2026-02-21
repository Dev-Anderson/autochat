from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import engine, Base, SessionLocal
from app.models import User, Company
from app.schemas import (
    UserCreate,
    LoginRequest,
    CompanyCreate,
    UserResponse,
    CompanyResponse,
)
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    require_super_admin,
    require_company_admin,
)

app = FastAPI()


# 🚀 cria tabelas no startup (MVP)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # 👑 verifica se já existe um super admin
    super_admin = db.query(User).filter(User.role == "super_admin").first()

    if not super_admin:
        user = User(
            name="Admin",
            email="admin@autochat.com",
            hashed_password=hash_password("admin123"),
            role="super_admin",
            company_id=None
        )

        db.add(user)
        db.commit()

    db.close()


# 🔌 conexão com banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "AutoChat rodando 🚀"}


# 👑 criar usuário (apenas super admin)
@app.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin),
):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role="super_admin",  # default criando usuários admin do sistema
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# 🔐 login
@app.post("/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Senha inválida")

    token = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# 📥 listar usuários (apenas super admin)
@app.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin),
):
    return db.query(User).all()


# ❌ deletar usuário (apenas super admin)
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(user)
    db.commit()

    return {"message": "Usuário deletado com sucesso"}


# 🏢 criar empresa + admin da empresa (apenas super admin)
@app.post("/companies", response_model=CompanyResponse)
def create_company(
    data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin),
):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    company = Company(name=data.company_name)
    db.add(company)
    db.commit()
    db.refresh(company)

    user = User(
        name=data.user_name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role="company_admin",
        company_id=company.id,
    )

    db.add(user)
    db.commit()

    return company


# 📥 listar empresas (super admin)
@app.get("/companies", response_model=list[CompanyResponse])
def list_companies(
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin),
):
    return db.query(Company).all()