from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import Column, Integer, String, Enum, Table, ForeignKey, Boolean, DateTime

from src.db.database import DbBaseModel
from src.utils.enumerations import Role


USER_has_TAG = Table(
    'user_has_tag',
    DbBaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('is_shown', Boolean, default=False, nullable=False),
    Column('created_at', DateTime(timezone=True), default=func.now()),
    Column('updated_at', DateTime(timezone=True), default=func.now(), onupdate=func.now()),
)


USER_saves_TOPIC = Table(
    'user_saves_topic',
    DbBaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('topic_id', Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('created_at', DateTime(timezone=True), default=func.now()),
    Column('updated_at', DateTime(timezone=True), default=func.now(), onupdate=func.now()),
)


TOPIC_has_CATEGORY = Table(
    'topic_has_category',
    DbBaseModel.metadata,
    Column('topic_id', Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('created_at', DateTime(timezone=True), default=func.now()),
    Column('updated_at', DateTime(timezone=True), default=func.now(), onupdate=func.now()),
)


class UserRatesComment(DbBaseModel):
    __tablename__ = 'user_rates_comment'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    comment_id = Column(Integer, ForeignKey('comments.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    rating = Column(Integer, nullable=False)

    user = relationship('User', back_populates='rated_comments')
    comment = relationship('Comment', back_populates='rated_by')


class UserRatesTopic(DbBaseModel):
    __tablename__ = 'user_rates_topic'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    rating = Column(Integer, nullable=False)

    user = relationship('User', back_populates='rated_topics')
    topic = relationship('Topic', back_populates='rated_by')


class User(DbBaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(Enum(Role), nullable=False)
    password = Column(String, nullable=False)

    tags = relationship('Tag', secondary=USER_has_TAG, back_populates='users')
    topics = relationship('Topic', back_populates='author')
    rated_topics = relationship('UserRatesTopic', back_populates='user')
    saved_topics = relationship('Topic', secondary=USER_saves_TOPIC, back_populates='saved_by')
    comments = relationship('Comment', back_populates='author')
    rated_comments = relationship('UserRatesComment', back_populates='user')


class Tag(DbBaseModel):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    users = relationship('User', secondary=USER_has_TAG, back_populates='tags')


class Comment(DbBaseModel):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    is_fixed = Column(Boolean, default=False, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    rating = column_property(
        select(func.coalesce(func.sum(UserRatesComment.rating), 0))
        .filter(UserRatesComment.comment_id == id)
        .correlate_except(UserRatesComment)
        .scalar_subquery()
    )

    author = relationship('User', back_populates='comments')
    files = relationship('File', back_populates='comment')
    topic = relationship('Topic', back_populates='comments')
    rated_by = relationship('UserRatesComment', back_populates='comment')


class Topic(DbBaseModel):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_fixed = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    rating = column_property(
        select(func.coalesce(func.sum(UserRatesTopic.rating), 0))
        .filter(UserRatesTopic.topic_id == id)
        .correlate_except(UserRatesTopic)
        .scalar_subquery()
    )
    comments_count = column_property(
        select(func.count(Comment.id))
        .where(Comment.topic_id == id)
        .correlate_except(Comment)
        .scalar_subquery()
    )

    files = relationship('File', back_populates='topic')
    author = relationship('User', back_populates='topics')
    comments = relationship('Comment', back_populates='topic')
    categories = relationship('Category', secondary=TOPIC_has_CATEGORY, back_populates='topics')
    saved_by = relationship('User', secondary=USER_saves_TOPIC, back_populates='saved_topics')
    rated_by = relationship('UserRatesTopic', back_populates='topic')

    def user_has_liked_topic(self, db_session: Session, user_id: int) -> bool:
        return bool(db_session.query(UserRatesTopic).filter_by(
            user_id=user_id, topic_id=self.id, rating=1).one_or_none())

    def user_has_disliked_topic(self, db_session: Session, user_id: int) -> bool:
        return bool(db_session.query(UserRatesTopic).filter_by(
            user_id=user_id, topic_id=self.id, rating=-1).one_or_none())


class Category(DbBaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    color = Column(String, nullable=True)

    topics = relationship('Topic', secondary=TOPIC_has_CATEGORY, back_populates='categories')


class File(DbBaseModel):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    upload_path = Column(String, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=True)
    comment_id = Column(Integer, ForeignKey('comments.id', ondelete='CASCADE'), nullable=True)

    topic = relationship('Topic', back_populates='files')
    comment = relationship('Comment', back_populates='files')
