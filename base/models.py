import datetime
import uuid

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.types import Boolean

from base import db
from base.custom_sql_fields import ChoiceType, JSONEncodedDict

class HootenflattenBaseObject(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True))
    
    def __init__(self):
        self.id = uuid.uuid4()
        self.created_at = datetime.datetime.utcnow()

class Comment(db.Model, HootenflattenBaseObject):
    __tablename__ = "comment"
    
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True))
    user_id = Column(Integer, ForeignKey('user.id'))
    
    user = relationship("User")

    def __repr__(self):
        return "<Comment: %r - %r>" % (self.comment, self.user_id)

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

class Extension(db.Model):
    __tablename__ = 'extensions'

    id = Column(Integer, primary_key=True)
    extension_name = Column(String(200))
    configured = Column(Boolean)
    version = Column(Float)

    def __repr__(self):
        return "<Extension: %r - Configured: %r>" % (self.extension_name, self.configured)

class CustomQuestion(db.Model):
    __tablename__ = 'custom_questions'
    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    name = Column(String(50))
    question = Column(Text)
    validators = Column(JSONEncodedDict(255))  # ex: ['Required', 'Email']
    choices = Column(JSONEncodedDict(255)) # ex: [(1,'Hello'),(2,'GoodBye')]
    widget = Column(ChoiceType((
                         ("TextField","TextField"),
                         ("TextAreaField", "TextAreaField"),
                         ("BooleanField", "BooleanField"),
                         ("DateField", "DateField"),
                         ("DateTimeField", "DateTimeField"),
                         ("Floatfield", "FloatField"),
                         ("IntegerField", "IntegerField"),
                         ("RadioField", "RadioField"),
                         ("SelectField", "SelectField"),
                         ("SelectMultipleField","SelectMultipleField")
                        )))


db.create_all()