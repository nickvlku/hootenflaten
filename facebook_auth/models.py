import uuid

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from base import db
from base.models import HootenflattenBaseObject


class FacebookUser(db.Model, HootenflattenBaseObject):
    __tablename__ = "facebook_user"

    id = Column(Integer, primary_key=True)
    access_token = Column(String(200))
    first_name = Column(String(200))
    last_name = Column(String(200))
    user_name = Column(String(200))
    facebook_id = Column(Integer)
    created_at = Column(DateTime(timezone=True))
    email = Column(String(200))
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User")

    def __repr__(self):
        return "<FacebookUser %r>" % self.user_name


db.create_all()