from flask.ext.mail import Mail
import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore,\
    UserMixin, RoleMixin
from flask.ext.mustache import FlaskMustache

from flaskext.themes import setup_themes, load_themes_from, packaged_themes_loader, theme_paths_loader
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import case
from base.custom_sql_fields import JSONEncodedDict, SecurityTrackable
from base.extensions import init_extensions

from Configurator import Configurator


app = Flask(__name__)
app.config.from_object('base.default_settings.Config')
try:
    app.config.from_envvar('HOOTENFLATEN_SETTINGS')
except RuntimeError:
    app.logger.warning("You have not specified a HOOTENFLATEN_SETTINGS environment variable.  You have no overrides from the default")

db = SQLAlchemy(app)
FlaskMustache(app)
mail = Mail(app)


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



def instance_loader(app):
    base_app_path = os.path.split(app.root_path)[0]

    themes_dir = os.path.join(base_app_path, 'themes')
    if os.path.isdir(themes_dir):
        return load_themes_from(themes_dir)
    else:
        return ()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

init_extensions(app)

configurator = Configurator(app)


setup_themes(app, app_identifier="hootenflaten", loaders=[instance_loader, packaged_themes_loader, theme_paths_loader])


import base.view_helpers
import base.views
import base.models

from time import mktime

app.jinja_env.filters['mktime'] = mktime