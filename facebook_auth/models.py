from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql import case

from base.database import db
from base.models import HootenflattenBaseObject


class FacebookUser(HootenflattenBaseObject, db.Model):
    __tablename__ = "facebook_user"

    access_token = Column(String(200))
    first_name = Column(String(200))
    last_name = Column(String(200))
    user_name = Column(String(200))
    facebook_id = Column(Integer)
    email = Column(String(200))
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User")

    def __repr__(self):
        return "<FacebookUser %r>" % self.user_name

    @hybrid_property
    def full_name(self):
        if self.first_name is not None:
            return self.first_name + " " + self.last_name
        else:
            return self.last_name

    @full_name.expression
    def full_name(cls):
        return case([
            (cls.first_name != None, cls.first_name + " " + cls.last_name),
        ], else_ = cls.last_name)


    def __init__(self, access_token, first_name, last_name, facebook_id, user_name, email):
        super(FacebookUser,self).__init__()
        self.access_token = access_token
        self.first_name = first_name
        self.last_name = last_name
        self.facebook_id = facebook_id
        self.user_name = user_name
        self.email = email

