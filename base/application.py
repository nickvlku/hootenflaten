from logging.handlers import RotatingFileHandler
from time import mktime
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, logging
from flask.ext.themes import load_themes_from, setup_themes, packaged_themes_loader, theme_paths_loader
from flask.ext.security import SQLAlchemyUserDatastore

import os
from base.database import init_db


def create_app():
    app = Flask("hootenflaten")
    init_db(app)  # we first init the db


    configure_app(app)
    configure_flask_extensions(app)
    configure_theme_manager(app)
    configure_security(app)
    configure_jinja_filters(app)
    #configure_errorhandlers(app)
    configure_logging(app)
    configure_root(app)

    return app

def configure_app(app):

    app.config.from_object('base.default_settings.Config')
    try:
        app.config.from_envvar('HOOTENFLATEN_SETTINGS')
    except RuntimeError:
        app.logger.warning("You have not specified a HOOTENFLATEN_SETTINGS environment variable.  You have no overrides from the default")


def configure_flask_extensions(app):
    from base.flask_extensions import mustache, mail, configurator
    mustache.init_app(app)
    mail.init_app(app)
    configurator.init_app(app)

def configure_theme_manager(app):

    def instance_loader(app):
        base_app_path = os.path.split(app.root_path)[0]

        themes_dir = os.path.join(base_app_path, 'themes')
        if os.path.isdir(themes_dir):
            return load_themes_from(themes_dir)
        else:
            return ()

    setup_themes(app, app_identifier="hootenflaten",
        loaders=[instance_loader, packaged_themes_loader, theme_paths_loader])

def configure_security(app):
    from base.database import db
    from base.flask_extensions import security
    from hootenflaten_auth.models import User, Role

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

def configure_jinja_filters(app):
    app.jinja_env.filters['mktime'] = mktime

def configure_errorhandlers(app):

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error='Sorry, page not found')
        return render_template("errors/404.html", error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error='Sorry, not allowed')
        return render_template("errors/403.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error='Sorry, an error has occurred')
        return render_template("errors/500.html", error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonify(error="Login required")
        flash("Please login to see this page")
        return redirect(url_for("account.login", next=request.path))


def configure_logging(app):
    if app.debug or app.testing:
        return


    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join(app.root_path,
        app.config['DEBUG_LOG'])

    debug_file_handler =\
    RotatingFileHandler(debug_log,
        maxBytes=100000,
        backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path,
        app.config['ERROR_LOG'])

    error_file_handler =\
    RotatingFileHandler(error_log,
        maxBytes=100000,
        backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

def configure_root(app):
    from base.views import root_views
    app.register_blueprint(root_views)