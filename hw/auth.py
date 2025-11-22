from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
import secrets
import hashlib

from hw_SQLAlchemy_Alembic import Base, engine, Session as SessionMaker

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=True)


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    user_token: str
    message: str


Base.metadata.create_all(engine)


auth_router = APIRouter(prefix="/auth", tags=["aутентификация"])


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()


@auth_router.post("/register", response_model=TokenResponse, status_code=201)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="пользователь с таким именем уже существует")

    password_hash = hash_password(user_data.password)
    token = generate_token()

    new_user = User(
        username=user_data.username,
        password_hash=password_hash,
        token=token
    )

    db.add(new_user)
    db.commit()

    return TokenResponse(
        user_token=token,
        message="пользователь успешно зарегистрирован"
    )


@auth_router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="неверное имя пользователя или пароль")

    password_hash = hash_password(user_data.password)
    if user.password_hash != password_hash:
        raise HTTPException(status_code=401, detail="неверное имя пользователя или пароль")

    token = generate_token()
    user.token = token
    db.commit()

    return TokenResponse(
        user_token=token,
        message="вход выполнен успешно"
    )


@auth_router.post("/logout")
def logout(user_token: str = Header(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.token == user_token).first()
    if not user:
        raise HTTPException(status_code=401, detail="недействительный токен")

    user.token = None
    db.commit()

    return {"выход выполнен успешно"}


def verify_token(user_token: str = Header(...), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.token == user_token).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="требуется авторизация"
        )
    return user