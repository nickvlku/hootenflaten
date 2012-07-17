import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import (User, Security, LoginForm,  login_required,
                                roles_accepted, user_datastore)
from flask.ext.security.datastore.sqlalchemy import SQLAlchemyUserDatastore

from flaskext.themes import setup_themes, load_themes_from, packaged_themes_loader, theme_paths_loader
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import case
from base.custom_sql_fields import JSONEncodedDict
from base.extensions import init_extensions


app = Flask(__name__)
app.config.from_object('base.default_settings.Config')
try:
    app.config.from_envvar('HOOTENFLATEN_SETTINGS')
except RuntimeError:
    app.logger.warning("You have not specified a HOOTENFLATEN_SETTINGS environment variable.  You have no overrides from the default")

db = SQLAlchemy(app)

class UserAccountMixin():
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    custom_questions_json = db.Column(JSONEncodedDict(255))
    ran_through_first_run_wizard = db.Column(db.Boolean)
    profile_image = db.Column(db.String(255))

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


security = Security(app, SQLAlchemyUserDatastore(db, UserAccountMixin))

init_extensions(app)

def instance_loader(app):
    base_app_path = os.path.split(app.root_path)[0]

    themes_dir = os.path.join(base_app_path, 'themes')
    if os.path.isdir(themes_dir):
        return load_themes_from(themes_dir)
    else:
        return ()


setup_themes(app, app_identifier="hootenflaten", loaders=[instance_loader, packaged_themes_loader, theme_paths_loader])


import base.view_helpers
import base.views
import base.models
