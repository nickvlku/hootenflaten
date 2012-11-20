from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mustache import FlaskMustache
from flask.ext.security import Security


__all__ = ['mail', 'mail', 'mustache', 'configurator', 'security']

mail = Mail()
db = SQLAlchemy()
mustache = FlaskMustache()

from Configurator import Configurator
configurator = Configurator()

security = Security()
