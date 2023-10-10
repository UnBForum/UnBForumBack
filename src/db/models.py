from sqlalchemy import Column, Integer, String, Enum, Table, ForeignKey, \
    Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

from src.utils.enumerations import Role


Base = declarative_base()


user_has_tag = Table(
    'user_has_tag',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False, primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), nullable=False, primary_key=True),
    Column('is_shown', Boolean, nullable=False),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now()),
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(Enum(Role), nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tags = relationship('Tag', secondary=user_has_tag, back_populates='users')


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    users = relationship('User', secondary=user_has_tag, back_populates='tags')
