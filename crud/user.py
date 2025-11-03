from sqlalchemy.orm import Session
from models import User
from auth import hash_password, verify_password
from database import get_session

def create_user(db: Session, username: str, password: str):
    hashed = hash_password(password)
    user = User(username=username, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter_by(username=username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user
