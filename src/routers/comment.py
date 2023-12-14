from typing import List

from fastapi import APIRouter, Depends, status, Response, Security
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.db.models import Comment, User, UserRatesComment
from src.routers.deps import get_db_session, get_authenticated_user, check_permission
from src.schemas.comment import CommentCreateSchema, CommentRetrieveSchema, CommentRatingSchema
from src.utils.enumerations import Role


comment_router = APIRouter(prefix='/topics/{topic_id:int}/comments', tags=['Comment'])


@comment_router.post('/', status_code=status.HTTP_201_CREATED, response_model=CommentRetrieveSchema)
def create_comment(
        topic_id: int,
        comment: CommentCreateSchema,
        db_session: Session = Depends(get_db_session),
        current_user: User = Depends(get_authenticated_user)
):
    comment_on_db = Comment(**comment.model_dump(exclude={'files'}), topic_id=topic_id, user_id=current_user.id)
    try:
        comment_on_db.save(db_session)
        return comment_on_db
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Erro ao criar o comentário',
        )


@comment_router.get('/', response_model=List[CommentRetrieveSchema])
def get_all_topic_comments(topic_id: int, db_session: Session = Depends(get_db_session)):
    comments = Comment.get_all(db_session, topic_id=topic_id)
    return comments


@comment_router.get('/{comment_id:int}', response_model=CommentRetrieveSchema)
def get_comment(topic_id: int, comment_id: int, db_session: Session = Depends(get_db_session)):
    comment = get_comment_or_raise_exception(comment_id, topic_id, db_session)
    return comment

@comment_router.put('/{comment_id:int}')
def update_comment(
        topic_id: int,
        comment_id: int,
        comment: CommentCreateSchema,
        db_session: Session = Depends(get_db_session), current_user: User = Depends(get_authenticated_user)
):
    comment_on_db = get_comment_or_raise_exception(comment_id, topic_id, db_session)
    if comment_on_db.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Você não tem permissão para realizar esta ação',
        )

    try:
        comment_on_db.update(db_session, **comment.model_dump())
        return comment_on_db
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Erro ao atualizar o comentário',
        )



@comment_router.delete('/{comment_id:int}')
def delete_comment(
        topic_id: int,
        comment_id: int,
        db_session: Session = Depends(get_db_session),
        current_user: User = Depends(get_authenticated_user)
):
    comment = get_comment_or_raise_exception(comment_id, topic_id, db_session)
    if comment.user_id != current_user.id and current_user.role not in (Role.moderator, Role.administrator):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Você não tem permissão para realizar esta ação',
        )
    comment.delete(db_session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@comment_router.post(
    '/{comment_id:int}/fix',
    dependencies=[Security(check_permission, scopes=[Role.moderator, Role.administrator])]
)
def fix_comment(
        topic_id: int,
        comment_id: int,
        db_session: Session = Depends(get_db_session)
):
    comment = get_comment_or_raise_exception(comment_id, topic_id, db_session)
    comment.update(db_session, is_fixed=not comment.is_fixed)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@comment_router.post('/{comment_id:int}/upvote', response_model=CommentRatingSchema)
def upvote_comment(
        topic_id: int,
        comment_id: int,
        db_session: Session = Depends(get_db_session),
        current_user: User = Depends(get_authenticated_user)
):
    comment = get_comment_or_raise_exception(comment_id, topic_id, db_session)

    if comment.user_has_liked_comment(db_session, current_user.id):
        # Se o usuário já havia avaliado o comentário positivamente, remove a avaliação
        user_rating = UserRatesComment.get_one(db_session, user_id=current_user.id, comment_id=comment_id)
        user_rating.delete(db_session)
        comment.current_user_rating = 0
    else:
        # Se o usuário não havia avaliado o comentário positivamente, adiciona a avaliação
        user_rating = UserRatesComment(user_id=current_user.id, comment_id=comment_id, rating=1)
        try:
            user_rating.create_or_update(db_session)
            comment.current_user_rating = 1
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro ao avaliar comentário',
            )

    return comment


@comment_router.post('/{comment_id:int}/downvote', response_model=CommentRatingSchema)
def downvote_comment(
        topic_id: int,
        comment_id: int,
        db_session: Session = Depends(get_db_session),
        current_user: User = Depends(get_authenticated_user)
):
    comment = get_comment_or_raise_exception(comment_id, topic_id, db_session)

    if comment.user_has_disliked_comment(db_session, current_user.id):
        # Se o usuário já havia avaliado o comentário negativamente, remove a avaliação
        user_rating = UserRatesComment.get_one(db_session, user_id=current_user.id, comment_id=comment_id)
        user_rating.delete(db_session)
        comment.current_user_rating = 0
    else:
        # Se o usuário não havia avaliado o comentário negativamente, adiciona a avaliação
        user_rating = UserRatesComment(user_id=current_user.id, comment_id=comment_id, rating=-1)
        try:
            user_rating.create_or_update(db_session)
            comment.current_user_rating = -1
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro ao avaliar comentário',
            )

    return comment


def get_comment_or_raise_exception(comment_id: int, topic_id: int, db_session: Session) -> Comment:
    comment = Comment.get_one(db_session, id=comment_id, topic_id=topic_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Comentário não encontrado',
        )
    return comment
