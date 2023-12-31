from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import APIRouter, Depends, status, Response, Security
from fastapi.exceptions import HTTPException
from fastapi_filter import FilterDepends

from src.db.models import Topic, Category, User, File, TOPIC_has_CATEGORY, UserRatesTopic
from src.schemas.topic import (TopicCreateSchema, TopicRetrieveSchema, TopicWithCommentsSchema,
                               TopicUpdateSchema, TopicFilterSchema, TopicRatingSchema)
from src.routers.deps import get_db_session, get_authenticated_user, check_permission, get_current_user
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
    for file_id in topic.files:
        file_on_db = File.get_one(db_session, id=file_id)
        if not file_on_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Erro ao criar o tópico. Arquivo não existe',
            )
        topic_on_db.files.append(file_on_db)
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
        db_session: Session = Depends(get_db_session),
        current_user: User | None = Depends(get_current_user)
):
    query = db_session.query(Topic).outerjoin(TOPIC_has_CATEGORY).outerjoin(Category)
    query = topic_filter.filter(query)
    query = topic_filter.sort(query)

    topics = []
    for topic in query.all():
        topic.fill_current_user_information(db_session, getattr(current_user, 'id', -1))
        topics.append(topic)
    return topics


@topic_router.get('/{topic_id:int}', response_model=TopicWithCommentsSchema)
def get_one_topic(
        topic_id: int,
        db_session: Session = Depends(get_db_session),
        current_user: User | None = Depends(get_current_user)
):
    topic = get_topic_or_raise_exception(topic_id, db_session)
    topic.fill_current_user_information(db_session, getattr(current_user, 'id', -1))
    topic.comments = topic.comments_with_current_user_rating(db_session, getattr(current_user, 'id', -1))
    return topic


@topic_router.put('/{topic_id:int}', response_model=TopicRetrieveSchema)
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

    categories = []
    for category_id in topic.categories:
        category_on_db = Category.get_one(db_session, id=category_id)
        if not category_on_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Erro ao atualizar o tópico. Categoria não existe',
            )
        categories.append(category_on_db)

    files = []
    for file_id in topic.files:
        file_on_db = File.get_one(db_session, id=file_id)
        if not file_on_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Erro ao atualizar o tópico. Arquivo não existe',
            )
        files.append(file_on_db)

    try:
        topic_on_db.categories = categories
        topic_on_db.files = files
        topic_on_db.update(db_session, **topic.model_dump(exclude={'categories', 'files'}))
        return topic_on_db
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Erro ao atualizar o tópico')


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
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Tópico já salvo',
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@topic_router.post('/{topic_id:int}/unsave')
def unsave_topic(
        topic_id: int,
        db_session: Session = Depends(get_db_session),
        current_user: User = Depends(get_authenticated_user)
):
    topic = get_topic_or_raise_exception(topic_id, db_session)
    try:
        current_user.saved_topics.remove(topic)
        current_user.save(db_session)
    except ValueError or SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Erro ao deixar de salvar tópico',
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
        topic.current_user_rating = 0
    else:
        # Se o usuário não havia avaliado o tópico positivamente, adiciona a avaliação
        user_rating = UserRatesTopic(user_id=current_user.id, topic_id=topic_id, rating=1)
        try:
            user_rating.create_or_update(db_session)
            topic.current_user_rating = 1
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
        topic.current_user_rating = 0
    else:
        # Se o usuário não havia avaliado o tópico negativamente, adiciona a avaliação
        user_rating = UserRatesTopic(user_id=current_user.id, topic_id=topic_id, rating=-1)
        try:
            user_rating.create_or_update(db_session)
            topic.current_user_rating = -1
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro ao avaliar tópico',
            )

    return topic


@topic_router.post(
    '/{topic_id:int}/fix',
    dependencies=[Security(check_permission, scopes=[Role.moderator, Role.administrator])]
)
def fix_topic(
        topic_id: int,
        db_session: Session = Depends(get_db_session)
):
    topic = get_topic_or_raise_exception(topic_id, db_session)
    topic.update(db_session, is_fixed=not topic.is_fixed)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_topic_or_raise_exception(topic_id: int, db_session: Session) -> Topic:
    topic = Topic.get_one(db_session, id=topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tópico não encontrado',
        )
    return topic
