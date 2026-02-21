# app/auth.py

from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db import SessionLocal
from app.models import User

# 🔐 configs JWT
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🔒 hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔑 esquema Bearer simples (Swagger vai permitir colar token)
security = HTTPBearer()


# 🔒 gerar hash da senha
def hash_password(password: str):
    return pwd_context.hash(password)


# 🔍 validar senha
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# 🎟️ criar token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 👤 obter usuário a partir do token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()

    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user


# 👑 somente super admin
def require_super_admin(user: User = Depends(get_current_user)):
    if user.role != "super_admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user


# 🏢 admin da empresa ou super admin
def require_company_admin(user: User = Depends(get_current_user)):
    if user.role not in ["super_admin", "company_admin"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user