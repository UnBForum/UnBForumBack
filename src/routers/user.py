from typing import List

from fastapi import status, Depends, APIRouter, Response, Security
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from src.routers.deps import get_db_session, get_authenticated_user, check_permission
from src.schemas.user import UserCreateSchema, UserRetrieveSchema, UserUpdateSchema, UserChangePasswordSchema
from src.schemas.topic import TopicRetrieveSchema
from src.db.models import User, Tag
from src.utils.enumerations import Role


crypt_context = CryptContext(schemes=['sha256_crypt'])
user_router = APIRouter(prefix='/users', tags=['User'])


@user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserRetrieveSchema)
def create_user(user: UserCreateSchema, db_session: Session = Depends(get_db_session)):
    user_on_db = User(
        password=crypt_context.hash(user.password),
        **user.model_dump(exclude={'password', 'tags'})
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


@user_router.get(
    '/',
    response_model=List[UserRetrieveSchema],
    dependencies=[Security(check_permission, scopes=[Role.administrator])]
)
def get_all_users(db_session: Session = Depends(get_db_session)):
    users = User.get_all(db_session)
    return users


@user_router.get(
    '/{user_id:int}',
    response_model=UserRetrieveSchema,
    dependencies=[Security(check_permission, scopes=[Role.administrator])]
)
def get_one_user(user_id: int, db_session: Session = Depends(get_db_session)):
    user = User.get_one(db_session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Usuário não encontrado',
        )
    return user


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


@user_router.post('/me/change_password')
def change_current_user_password(
    pass_schema: UserChangePasswordSchema,
    db_session: Session = Depends(get_db_session),
    current_user: User = Depends(get_authenticated_user)
):
    if not crypt_context.verify(pass_schema.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Senha atual incorreta',
        )
    current_user.update(db_session, password=crypt_context.hash(pass_schema.new_password))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@user_router.delete('/me')
def delete_current_user(
    db_session: Session = Depends(get_db_session),
    current_user: User = Depends(get_authenticated_user)
):
    current_user.delete(db_session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@user_router.get('/me/topics', response_model=List[TopicRetrieveSchema])
def get_current_user_topics(current_user: User = Depends(get_authenticated_user)):
    return current_user.topics
