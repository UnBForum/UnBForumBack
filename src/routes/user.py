from fastapi import status, Depends, APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from src.routes.deps import get_db_session, get_authenticated_user
from src.schemas.user import UserCreateSchema, UserRetrieveSchema, UserUpdateSchema, TokenData
from src.db.models import User
from src.utils.jwt import create_access_token


crypt_context = CryptContext(schemes=['sha256_crypt'])


user_router = APIRouter(prefix='/users')


@user_router.post('/')
def create_user(user: UserCreateSchema, db_session: Session = Depends(get_db_session)):
    user_on_db = User(
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


@user_router.post('/login', response_model=TokenData)
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


@user_router.get('/me', response_model=UserRetrieveSchema)
def get_current_user(current_user: User = Depends(get_authenticated_user)):
    return current_user


@user_router.patch('/me', response_model=UserRetrieveSchema)
def update_authenticated_user(
    update_data: UserUpdateSchema,
    db_session: Session = Depends(get_db_session),
    current_user: User = Depends(get_authenticated_user)
):
    for field, value in update_data.model_dump().items():
        if value is not None:
            setattr(current_user, field, value)

    db_session.commit()

    return current_user


@user_router.delete('/me')
def delete_authenticated_user(
    db_session: Session = Depends(get_db_session),
    current_user: User = Depends(get_authenticated_user)
):
    db_session.delete(current_user)
    db_session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
