import json
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import String

from base import db
from base.custom_sql_fields import ChoiceType, JSONEncodedDict
from base.models import HootenflattenBaseObject,IsCommentableMixin

Base = declarative_base()

status_user_awesome_table = db.Table('status_user_awesomes',
    db.Column('user_id', Integer, ForeignKey('user.id')),
    db.Column('status_id', String(45), ForeignKey('status.id')))


class StatusUpdate(HootenflattenBaseObject, IsCommentableMixin, db.Model):
    __tablename__ = "status"

    status_update = Column(Text)
    references_type = Column(ChoiceType((
        ("photo", "photo"),
        ("video", "video"),
        ("link", "link"),
        ("event", "event"),
        ("location", "location"),
        ("tweet", "tweet")
    )))

    reference_json = Column(JSONEncodedDict(255))

    awesome_list = db.relationship("User", secondary=status_user_awesome_table, backref=db.backref('awesomed_things', lazy='dynamic'))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    def __repr__(self):
        return "<StatusUpdate: %r: %r>" % (self.user_id, self.status_update)

    def to_json(self):
        if self.reference_json is None:
            ref_json = dict()
        else:
            ref_json = self.reference_json

        json_dict = dict(
            id = self.id,
            status_update = self.status_update,
            references_json = ref_json,
            awesomes = self.awesome_list,
            comments = self.comments,
            user = dict(
                id = self.user.id,
                full_name = self.user.full_name,
                profile_image = self.user.profile_image
            ),
            created_on = self.created_at.toordinal()
        )
        return json.dumps(json_dict)

db.create_all()