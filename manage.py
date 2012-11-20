from flask import current_app

from flask.ext.script import Manager, prompt, prompt_pass,\
    prompt_bool, prompt_choices
from base.application import create_app
from base.extensions import HootenflatenExtensionManager
from base.flask_extensions import db

manager = Manager(create_app)

@manager.command
def createall():
    "Creates database tables"
    db.create_all()
    HootenflatenExtensionManager(manager.app())

@manager.command
def dropall():
    "Drops all database tables"

    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()


if __name__ == "__main__":
    HootenflatenExtensionManager(manager.app())
    manager.run()

