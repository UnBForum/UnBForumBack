from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, status, Response, Security
from fastapi.exceptions import HTTPException

from src.db.models import Category
from src.schemas.category import CategoryCreateSchema, CategoryRetrieveSchema
from src.routers.deps import get_db_session, check_permission
from src.utils.enumerations import Role

category_router = APIRouter(prefix='/categories', tags=['Category'])


@category_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryRetrieveSchema,
    dependencies=[Security(check_permission, scopes=[Role.moderator, Role.administrator])],
)
def create_category(category: CategoryCreateSchema, db_session: Session = Depends(get_db_session)):
    category_on_db = Category(**category.model_dump())
    try:
        category_on_db.save(db_session)
        return category_on_db
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Erro ao criar a categoria',
        )


@category_router.get('/', response_model=List[CategoryRetrieveSchema])
def get_all_categories(db_session: Session = Depends(get_db_session)):
    categories = Category.get_all(db_session)
    return categories


@category_router.get('/{category_id}', response_model=CategoryRetrieveSchema)
def get_one_category(category_id: int, db_session: Session = Depends(get_db_session)):
    category = get_category_or_raise_exception(category_id, db_session)
    return category


@category_router.patch(
    '/{category_id:int}',
    response_model=CategoryRetrieveSchema,
    dependencies=[Security(check_permission, scopes=[Role.moderator, Role.administrator])],
)
def update_category(
        category_id: int,
        category: CategoryCreateSchema,
        db_session: Session = Depends(get_db_session)
):
    category_on_db = get_category_or_raise_exception(category_id, db_session)
    category_on_db.update(db_session, **category.model_dump(exclude_none=True))
    return category_on_db


@category_router.delete(
    '/{category_id:int}',
    dependencies=[Security(check_permission, scopes=[Role.moderator, Role.administrator])])
def delete_category(
        category_id: int,
        db_session: Session = Depends(get_db_session),
):
    category = get_category_or_raise_exception(category_id, db_session)
    category.delete(db_session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_category_or_raise_exception(category_id: int, db_session: Session):
    category = Category.get_one(db_session, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Categoria não encontrada',
        )
    return category
