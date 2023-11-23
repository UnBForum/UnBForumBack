from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException

from src.db.models import Topic, Category, User
from src.schemas.topic import TopicCreateSchema, TopicRetrieveSchema, TopicUpdateSchema
from src.routers.deps import get_db_session, get_authenticated_user
from src.utils.enumerations import Role

topic_router = APIRouter(prefix='/topics', tags=['Topic'])


@topic_router.post('/', status_code=status.HTTP_201_CREATED, response_model=TopicRetrieveSchema)
def create_topic(
        topic: TopicCreateSchema,
        db_session: Session = Depends(get_db_session),
        current_user = Depends(get_authenticated_user),
):
    topic_on_db = Topic(**topic.model_dump(exclude={'files', 'categories'}), user_id=current_user.id)
    for category_id in topic.categories:
        category_on_db = Category.get_one(db_session, id=category_id)
        if not category_on_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Categoria {category_on_db.name} não existe',
            )
        topic_on_db.categories.append(category_on_db)
    # for file in topic.files:
    #     file_on_db = File(name=file)
    #     topic_on_db.files.append(file_on_db)
    try:
        topic_on_db.save(db_session)
        return topic_on_db
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Erro ao criar o tópico',
        )


@topic_router.get('/', response_model=List[TopicRetrieveSchema])
def get_all_topics(db_session: Session = Depends(get_db_session)):
    topics = Topic.get_all(db_session)
    return topics


@topic_router.get('/{topic_id:int}', response_model=TopicRetrieveSchema)
def get_one_topic(topic_id: int, db_session: Session = Depends(get_db_session)):
    topic = get_topic_or_raise_exception(topic_id, db_session)
    return topic


@topic_router.patch('/{topic_id:int}', response_model=TopicRetrieveSchema)
def update_topic(
        topic_id: int,
        topic: TopicUpdateSchema,
        db_session: Session = Depends(get_db_session),
        current_user: User = Depends(get_authenticated_user)
):
    topic_on_db = get_topic_or_raise_exception(topic_id, db_session)
    if topic_on_db.user_id != current_user.id and current_user.role not in (Role.moderator, Role.administrator):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Você não tem permissão para realizar esta ação',
        )
    topic_on_db.update(db_session, **topic.model_dump(exclude_none=True))
    return topic_on_db


@topic_router.delete('/{topic_id:int}')
def delete_topic(
        topic_id: int,
        db_session: Session = Depends(get_db_session),
        current_user: User = Depends(get_authenticated_user)
):
    topic = get_topic_or_raise_exception(topic_id, db_session)
    if topic.user_id != current_user.id and current_user.role not in (Role.moderator, Role.administrator):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Você não tem permissão para realizar esta ação',
        )
    topic.delete(db_session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_topic_or_raise_exception(topic_id: int, db_session: Session) -> Topic:
    topic = Topic.get_one(db_session, id=topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tópico não encontrado',
        )
    return topic

