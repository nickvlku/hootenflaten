from flask import Blueprint

__author__ = 'nick'
__all__ = ('Configurator',)

configurator_app = Blueprint('configurator', __name__, template_folder='templates', static_folder='static')


from .models import ConfigurationSetting

class Configurator(object):
    def __init__(self, app=None, db=None):
        self.app = app
        self.db = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.register_blueprint(configurator_app, url_prefix="/_configure")
        from .models import db
        db.create_all(app=app)
