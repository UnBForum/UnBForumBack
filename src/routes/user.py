from fastapi import status, Depends, APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from src.routes.deps import get_db_session
from src.schemas.user import User, TokenData
from src.db.models import User as UserModel
from src.utils.jwt import create_access_token


crypt_context = CryptContext(schemes=['sha256_crypt'])


user_router = APIRouter(prefix='/users')


@user_router.post('/')
def create_user(user: User, db_session: Session = Depends(get_db_session)):
    user_on_db = UserModel(
        password=crypt_context.hash(user.password),
        **user.model_dump(exclude=['id', 'password'])
    )

    db_session.add(user_on_db)
    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email já cadastrado'
        )

    return Response(status_code=status.HTTP_201_CREATED)


@user_router.post('/login')
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session)
) -> TokenData:
    user_on_db = db_session.query(UserModel).filter_by(email=form_data.username).one_or_none()

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
