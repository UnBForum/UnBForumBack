from jose import jwt, JWTError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from decouple import config

from src.db.models import User

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')


def create_access_token(user_email: str):
    data = {"sub": user_email}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_token_n_get_user(token: str, db_session: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    user_email = data.get("sub")
    user = User.get_one(db_session, email=user_email)
    if not user:
        raise credentials_exception
    return user
