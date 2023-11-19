from sqlalchemy import Column, Integer, String, Enum, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.db.database import DbBaseModel
from src.utils.enumerations import Role


USER_has_TAG = Table(
    'user_has_tag',
    DbBaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('is_shown', Boolean, default=False, nullable=False),
)


USER_rates_TOPIC = Table(
    'user_rates_topic',
    DbBaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('topic_id', Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('rating', Integer, nullable=False),
)


USER_saves_TOPIC = Table(
    'user_saves_topic',
    DbBaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('topic_id', Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=False, primary_key=True),
)


TOPIC_has_CATEGORY = Table(
    'topic_has_category',
    DbBaseModel.metadata,
    Column('topic_id', Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False, primary_key=True),
)


class User(DbBaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(Enum(Role), nullable=False)
    password = Column(String, nullable=False)

    tags = relationship('Tag', secondary=USER_has_TAG, back_populates='users')
    topics = relationship('Topic', back_populates='user')
    comments = relationship('Comment', back_populates='user')


class Tag(DbBaseModel):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    users = relationship('User', secondary=USER_has_TAG, back_populates='tags')


class Topic(DbBaseModel):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_fixed = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    files = relationship('File', back_populates='topic')
    user = relationship('User', back_populates='topics')
    comments = relationship('Comment', back_populates='topic')
    categories = relationship('Category', secondary=TOPIC_has_CATEGORY, back_populates='topics')


class Category(DbBaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    color = Column(String, nullable=True)

    topics = relationship('Topic', secondary=TOPIC_has_CATEGORY, back_populates='categories')


class Comment(DbBaseModel):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    is_fixed = Column(Boolean, default=False, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    user = relationship('User', back_populates='comments')
    files = relationship('File', back_populates='comment')
    topic = relationship('Topic', back_populates='comments')


class File(DbBaseModel):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=False)
    comment_id = Column(Integer, ForeignKey('comments.id', ondelete='CASCADE'), nullable=False)

    topic = relationship('Topic', back_populates='files')
    comment = relationship('Comment', back_populates='files')
