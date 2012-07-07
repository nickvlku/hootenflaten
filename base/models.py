import datetime
import uuid

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from base import db

class HootenflattenBaseObject(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True))
    
    def __init__(self):
        self.id = uuid.uuid4()

class Comment(db.Model, HootenflattenBaseObject):
    __tablename__ = "comment"
    
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True))
    user_id = Column(Integer, ForeignKey('user.id'))
    
    user = relationship("User")

class IsCommentableMixin(object):

    @declared_attr
    def comments(cls):
        comment_association = Table(
            "%s_comments" % cls.__tablename__,
            cls.metadata,
            Column("comment_id", ForeignKey("comment.id"), primary_key=True),
            Column("%s_id" % cls.__tablename__, ForeignKey("%s.id" % cls.__tablename__),
            primary_key=True)
        )
        return relationship(Comment, secondary=comment_association, backref="%s_parents" % cls.__name__.lower())

