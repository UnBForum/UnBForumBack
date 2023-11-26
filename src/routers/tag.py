from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import APIRouter, Depends, status, Response, Security
from fastapi.exceptions import HTTPException

from src.db.models import Tag
from src.schemas.tag import TagCreateSchema, TagRetrieveSchema
from src.routers.deps import get_db_session, check_permission
from src.utils.enumerations import Role


tag_router = APIRouter(prefix='/tags', tags=['Tag'])


@tag_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=TagRetrieveSchema,
    dependencies=[Security(check_permission, scopes=[Role.moderator, Role.administrator])],
)
def create_tag(tag: TagCreateSchema, db_session: Session = Depends(get_db_session)):
    tag_on_db = Tag(**tag.model_dump())
    try:
        tag_on_db.save(db_session)
        return tag_on_db
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='A tag já existe')
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Erro ao criar a tag')


@tag_router.get('/', response_model=List[TagRetrieveSchema])
def get_all_tags(db_session: Session = Depends(get_db_session)):
    tags = Tag.get_all(db_session)
    return tags


@tag_router.get('/{tag_id:int}', response_model=TagRetrieveSchema)
def get_one_tag(tag_id: int, db_session: Session = Depends(get_db_session)):
    tag = get_tag_or_raise_exception(tag_id, db_session)
    return tag


@tag_router.delete(
    '/{tag_id:int}',
    dependencies=[Security(check_permission, scopes=[Role.moderator, Role.administrator])])
def delete_tag(tag_id: int,db_session: Session = Depends(get_db_session)):
    tag = get_tag_or_raise_exception(tag_id, db_session)
    tag.delete(db_session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_tag_or_raise_exception(tag_id: int, db_session: Session):
    tag = Tag.get_one(db_session, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tag não encontrada',
        )
    return tag
