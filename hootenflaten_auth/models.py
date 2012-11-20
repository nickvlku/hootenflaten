from sqlalchemy import case
from sqlalchemy.ext.hybrid import hybrid_property
from base.flask_extensions import db
from flask.ext.security import UserMixin, RoleMixin

from base.custom_sql_fields import JSONEncodedDict


class SecurityTrackable():
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.DateTime)
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    __tablename__ = "role"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin, SecurityTrackable):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    custom_questions_json = db.Column(JSONEncodedDict(255))
    ran_through_first_run_wizard = db.Column(db.Boolean)
    profile_image = db.Column(db.String(255))

    confirmed_at = db.Column(db.DateTime())

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

