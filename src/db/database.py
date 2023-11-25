from sqlalchemy import Column, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, Session


Base = declarative_base()


class DbBaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    @classmethod
    def get_one(cls, db_session: Session, **kwargs):
        try:
            return db_session.query(cls).filter_by(**kwargs).one_or_none()
        except SQLAlchemyError as e:
            db_session.rollback()
            raise e

    @classmethod
    def get_all(cls, db_session: Session, **kwargs):
        try:
            return db_session.query(cls).filter_by(**kwargs).all()
        except SQLAlchemyError as e:
            db_session.rollback()
            raise e

    def save(self, db_session: Session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            raise e

    def update(self, db_session: Session, **kwargs):
        try:
            for attr, value in kwargs.items():
                setattr(self, attr, value)
            db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            raise e

    def delete(self, db_session: Session):
        try:
            db_session.delete(self)
            db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            raise e

    @classmethod
    def delete_all(cls, db_session: Session):
        try:
            db_session.query(cls).delete()
            db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            raise e
