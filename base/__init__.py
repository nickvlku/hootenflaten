import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import (User, Security, LoginForm,  login_required,
                                roles_accepted, user_datastore)
from flask.ext.security.datastore.sqlalchemy import SQLAlchemyUserDatastore

from flaskext.themes import setup_themes, load_themes_from, packaged_themes_loader, theme_paths_loader
from base.extensions import init_extensions


app = Flask(__name__)
app.config.from_object('base.default_settings.Config')

db = SQLAlchemy(app)
Security(app, SQLAlchemyUserDatastore(db))

init_extensions(app)

def instance_loader(app):
    base_app_path = os.path.split(app.root_path)[0]

    themes_dir = os.path.join(base_app_path, 'themes')
    if os.path.isdir(themes_dir):
        return load_themes_from(themes_dir)
    else:
        return ()


setup_themes(app, app_identifier="hootenflaten", loaders=[instance_loader, packaged_themes_loader, theme_paths_loader])

try:
	app.config.from_envvar('HOOTENFLATEN_SETTINGS')
except RuntimeError:
	app.logger.warning("You have not specified a HOOTENFLATEN_SETTINGS environment variable.  You have no overrides from the default")


import base.views
import base.models
