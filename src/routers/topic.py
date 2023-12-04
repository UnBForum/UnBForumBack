from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import APIRouter, Depends, status, Response, Security
from fastapi.exceptions import HTTPException
from fastapi_filter import FilterDepends

from src.db.models import Topic, Category, User, TOPIC_has_CATEGORY, UserRatesTopic
from src.schemas.topic import (TopicCreateSchema, TopicRetrieveSchema, TopicRetrieveExtendedSchema,
                               TopicUpdateSchema, TopicFilterSchema, TopicRatingSchema)
from src.routers.deps import get_db_session, get_authenticated_user, check_permission
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
                detail=f'Erro ao criar o tópico. Categoria não existe',
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
def get_all_topics(
        topic_filter: TopicFilterSchema = FilterDepends(TopicFilterSchema),
        db_session: Session = Depends(get_db_session)
):
    query = db_session.query(Topic).outerjoin(TOPIC_has_CATEGORY).outerjoin(Category)
    query = topic_filter.filter(query)
    query = topic_filter.sort(query)
    topics = query.all()
    return topics


@topic_router.get('/{topic_id:int}', response_model=TopicRetrieveExtendedSchema)
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
    if topic_on_db.user_id != current_user.id:
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


@topic_router.post('/{topic_id:int}/save')
def save_topic(
        topic_id: int,
        db_session: Session = Depends(get_db_session),
        current_user: User = Depends(get_authenticated_user)
):
    topic = get_topic_or_raise_exception(topic_id, db_session)
    current_user.saved_topics.append(topic)
    try:
        current_user.save(db_session)
        # return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Tópico já salvo',
        )
    return Response(status_code=status.HTTP_200_OK)


@topic_router.post('/{topic_id:int}/upvote', response_model=TopicRatingSchema)
def upvote_topic(
        topic_id: int,
        db_session: Session = Depends(get_db_session),
        current_user: User = Depends(get_authenticated_user)
):
    topic = get_topic_or_raise_exception(topic_id, db_session)

    if topic.user_has_liked_topic(db_session, current_user.id):
        # Se o usuário já havia avaliado o tópico positivamente, remove a avaliação
        user_rating = UserRatesTopic.get_one(db_session, user_id=current_user.id, topic_id=topic_id)
        user_rating.delete(db_session)
    else:
        # Se o usuário não havia avaliado o tópico positivamente, adiciona a avaliação
        user_rating = UserRatesTopic(user_id=current_user.id, topic_id=topic_id, rating=1)
        try:
            user_rating.create_or_update(db_session)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro ao avaliar tópico',
            )

    return topic


@topic_router.post('/{topic_id:int}/downvote', response_model=TopicRatingSchema)
def downvote_topic(
        topic_id: int,
        db_session: Session = Depends(get_db_session),
        current_user: User = Depends(get_authenticated_user)
):
    topic = get_topic_or_raise_exception(topic_id, db_session)

    if topic.user_has_disliked_topic(db_session, current_user.id):
        # Se o usuário já havia avaliado o tópico negativamente, remove a avaliação
        user_rating = UserRatesTopic.get_one(db_session, user_id=current_user.id, topic_id=topic_id)
        user_rating.delete(db_session)
    else:
        # Se o usuário não havia avaliado o tópico negativamente, adiciona a avaliação
        user_rating = UserRatesTopic(user_id=current_user.id, topic_id=topic_id, rating=-1)
        try:
            user_rating.create_or_update(db_session)

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro ao avaliar tópico',
            )

    return topic


@topic_router.post(
    '/{topic_id:int}/fix',
    response_model=TopicRetrieveSchema,
    dependencies=[Security(check_permission, scopes=[Role.moderator, Role.administrator])]
)
def fix_topic(
        topic_id: int,
        db_session: Session = Depends(get_db_session)
):
    topic = get_topic_or_raise_exception(topic_id, db_session)
    topic.update(db_session, is_fixed=True)
    return topic


def get_topic_or_raise_exception(topic_id: int, db_session: Session) -> Topic:
    topic = Topic.get_one(db_session, id=topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tópico não encontrado',
        )
    return topic

