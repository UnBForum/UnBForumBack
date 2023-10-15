from fastapi import status, Depends, APIRouter, Response
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from src.routers.deps import get_db_session, get_authenticated_user
from src.schemas.user import UserCreateSchema, UserRetrieveSchema, UserUpdateSchema
from src.db.models import User


crypt_context = CryptContext(schemes=['sha256_crypt'])


user_router = APIRouter(prefix='/users', tags=['Account'])


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


@user_router.get('/me', response_model=UserRetrieveSchema)
def get_current_user(current_user: User = Depends(get_authenticated_user)):
    return current_user


@user_router.patch('/me', response_model=UserRetrieveSchema)
def update_current_user(
    update_data: UserUpdateSchema,
    db_session: Session = Depends(get_db_session),
    current_user: User = Depends(get_authenticated_user)
):
    for field, value in update_data.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)

    db_session.commit()

    return current_user


@user_router.delete('/me')
def delete_current_user(
    db_session: Session = Depends(get_db_session),
    current_user: User = Depends(get_authenticated_user)
):
    db_session.delete(current_user)
    db_session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
