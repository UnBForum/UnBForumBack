from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.db.connection import LocalSession
from src.utils.jwt import verify_token_n_get_user

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


def get_db_session():
    try:
        session = LocalSession()
        yield session
    finally:
        session.close()


def get_authenticated_user(
    db_session: Session = Depends(get_db_session),
    token: str = Depends(oauth_scheme)
):
    return verify_token_n_get_user(token, db_session)
