import uuid

from sqlalchemy.orm import Session

from models import User
from schemas import UserRegister
from core.security import hash_password, verify_password, create_access_token
from services.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError
)


def register_user(db: Session, data: UserRegister) -> User:
    existing_user = db.query(User).filter(User.username == data.username).first()

    if existing_user:
        raise UserAlreadyExistsError()

    user = User(username=data.username,hashed_password=hash_password(data.password))

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session,username: str,password: str) -> str:
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password,user.hashed_password):
        raise InvalidCredentialsError()

    return create_access_token(user.id)


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).first()