from fastapi import status, Depends, APIRouter, Response
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from src.routers.deps import get_db_session, get_authenticated_user
from src.schemas.user import UserCreateSchema, UserRetrieveSchema, UserUpdateSchema
from src.db.models import User, Tag


crypt_context = CryptContext(schemes=['sha256_crypt'])
user_router = APIRouter(prefix='/users', tags=['User'])


@user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserRetrieveSchema)
def create_user(user: UserCreateSchema, db_session: Session = Depends(get_db_session)):
    user_on_db = User(
        password=crypt_context.hash(user.password),
        **user.model_dump(exclude=['password', 'tags'])
    )
    for tag in user.tags:
        tag_on_db = Tag.get_one(db_session, name=tag)
        if not tag_on_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Tag {tag} não existe',
            )
        user_on_db.tags.append(tag_on_db)
    try:
        user_on_db.save(db_session)
        return user_on_db
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email já cadastrado',
        )


@user_router.get('/me', response_model=UserRetrieveSchema)
def get_current_user(current_user: User = Depends(get_authenticated_user)):
    return current_user


@user_router.patch('/me', response_model=UserRetrieveSchema)
def update_current_user(
    user: UserUpdateSchema,
    db_session: Session = Depends(get_db_session),
    current_user: User = Depends(get_authenticated_user)
):
    current_user.update(db_session, **user.model_dump(exclude_none=True))
    return current_user


@user_router.delete('/me')
def delete_current_user(
    db_session: Session = Depends(get_db_session),
    current_user: User = Depends(get_authenticated_user)
):
    current_user.delete(db_session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
