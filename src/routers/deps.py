from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from src.db.connection import LocalSession
from src.db.models import User
from src.utils.jwt import verify_token_n_get_user


oauth_scheme = OAuth2PasswordBearer(
    tokenUrl='/users/login',
    scopes={
        'member': 'Usuário membro',
        'moderator': 'Usuário moderador',
        'administrator': 'Usuário administrador'
    }
)

oauth_scheme_without_exception = OAuth2PasswordBearer(tokenUrl='/users/login', auto_error=False)


def get_db_session():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()


def get_authenticated_user(db_session: Session = Depends(get_db_session),token: str = Depends(oauth_scheme)):
    return verify_token_n_get_user(token, db_session)


def get_current_user(
        db_session: Session = Depends(get_db_session),
        token: str = Depends(oauth_scheme_without_exception)
):
    # Gets the current user or None if the user is not authenticated
    return verify_token_n_get_user(token, db_session) if token else None


def check_permission(security_scopes: SecurityScopes, current_user: User = Depends(get_authenticated_user)):
    if current_user.role not in security_scopes.scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Você não tem permissão para realizar esta ação',
        )
