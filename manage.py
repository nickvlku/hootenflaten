from flask import current_app

from flask.ext.script import Manager, prompt, prompt_pass,\
    prompt_bool, prompt_choices
from base.application import create_app
from base.database import db

app = create_app()
manager = Manager(app)

@manager.command
def createall():
    "Creates database tables"
    db.create_all()

@manager.command
def dropall():
    "Drops all database tables"

    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()


if __name__ == "__main__":
    from base.extensions import HootenflatenExtensionManager
    HootenflatenExtensionManager(app)
    manager.run()

