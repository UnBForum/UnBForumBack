from fastapi import status, Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.routers.deps import get_db_session
from src.schemas.auth import TokenData
from src.db.models import User
from src.utils.jwt import create_access_token


crypt_context = CryptContext(schemes=['sha256_crypt'])


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post('/login', response_model=TokenData)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session)
):
    user_on_db = db_session.query(User).filter_by(email=form_data.username).one_or_none()

    if not user_on_db or not crypt_context.verify(form_data.password, user_on_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email ou senha inválidos'
        )

    access_token = create_access_token(user_on_db.email)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "access_token": access_token,
            "token_type": "bearer"
        }
    )
