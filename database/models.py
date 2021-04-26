
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
import datetime as dt


Base = declarative_base()

class IdMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)


class NameMixin:
    name = Column(String, nullable=False)


class UrlMixin:
    url = Column(String, nullable=False, unique=True)


tag_post = Table(
    'tag_post',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('tag_id', Integer, ForeignKey('tag.id')),
)


class Post(Base, UrlMixin):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    image = Column(String, nullable=False)
    publication_date = Column(DateTime)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author')
    tags = relationship('Tag', secondary=tag_post)
    comments = relationship('Comment')


class Author(Base, NameMixin, UrlMixin):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=False)
    posts = relationship(Post)


class Tag(Base, IdMixin, NameMixin, UrlMixin):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=False)
    posts = relationship(Post, secondary=tag_post)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('comment.id'), nullable=True)
    body = Column(String)
    created_at = Column(DateTime, nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author')
    post_id = Column(Integer, ForeignKey('post.id'))



    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.parent_id = kwargs['parent_id']
        self.body = kwargs['body']
        self.created_at = dt.datetime.fromisoformat(kwargs['created_at'])
        self.author_id = kwargs['user']['id']
        self.post_id = kwargs['post_id']
        self.author = kwargs['author']