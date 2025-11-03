from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import UserCreate, UserLogin
from crud.user import create_user, authenticate_user
from auth import create_access_token, get_current_user
from models import User

router = APIRouter(prefix="/api/v1", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(username=user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    user_obj = create_user(db, user.username, user.password)
    return {"msg": "Usuário criado com sucesso!", "id": user_obj.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token(str(db_user.id))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/auth/refresh")
def refresh_token(user_id: str = Depends(get_current_user)):
    new_token = create_access_token(user_id)
    return {"access_token": new_token, "token_type": "bearer"}
