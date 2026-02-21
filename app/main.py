from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import engine, Base, SessionLocal
from app.models import User, Company
from app.schemas import UserCreate

app = FastAPI()

# cria as tabelas automaticamente (MVP mode)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "AutoChat rodando 🚀"}


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    company = Company(name="Minha Empresa")
    db.add(company)
    db.commit()
    db.refresh(company)

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        company_id=company.id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user