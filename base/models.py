import datetime
import uuid
import hashlib
import json

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.types import Boolean

from base import db
from base.custom_sql_fields import ChoiceType, JSONEncodedDict

from flask import current_app

class HootenflattenBaseObject(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.String(42), primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True))
    hootenflaten_site_id = db.Column(db.String(42))
    active = db.Column(db.Boolean())

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()
        self.hootenflaten_site_id = hashlib.md5(current_app.config['SHORT_NAME']).hexdigest()
        self.active = True


# TODO: Need to abstract this out to an IsAwesomeableMixin
comment_user_awesome_table = db.Table('comment_user_awesomes',
    db.Column('user_id', Integer, ForeignKey('user.id')),
    db.Column('comment_id', String(45), ForeignKey('comment.id')))

class Comment(HootenflattenBaseObject, db.Model):
    __tablename__ = "comment"
    
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))

    awesome_list = db.relationship("User", secondary=comment_user_awesome_table, backref=db.backref('awesomed_comments', lazy='dynamic'))

    user = relationship("User")

    def __repr__(self):
        return "<Comment: %r - %r>" % (self.comment, self.user_id)

    def to_dict(self):
        comment_dict = dict(
            id = self.id,
            comment = self.comment,
            user = dict(
                id = self.user.id,
                full_name = self.user.full_name,
                profile_image = self.user.profile_image,
                first_name = self.user.first_name,
                last_name = self.user.last_name,
            ),
            created_on = self.created_at.toordinal(),
            awesome_list = []
        )

        for user in self.awesome_list:
            comment_dict['awesome_list'].append({
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': user.full_name,
                'profile_image': user.profile_image
            })

        return comment_dict

    def to_json(self):
        return json.dumps(self.to_dict())



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
        return relationship(Comment, order_by="Comment.created_at", secondary=comment_association, backref="%s_parents" % cls.__name__.lower())

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


    def __repr__(self):
        return "<Custom Question: %r: %r>" % (self.name, self.question)


db.create_all()