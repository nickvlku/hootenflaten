from flask import current_app

from flask.ext.script import Manager, prompt, prompt_pass,\
    prompt_bool, prompt_choices, Server
import sys
from base.application import create_app

app = create_app()
manager = Manager(app)

@manager.command
def createall():
    from base.database import db
    from base.extensions import HootenflatenExtensionManager
    db.create_all()

    HootenflatenExtensionManager(app)
    db.create_all()

@manager.command
def dropall():
    "Drops all database tables"
    from base.database import db
    from base.extensions import HootenflatenExtensionManager
    HootenflatenExtensionManager(app)
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()


if __name__ == "__main__":
    from base.extensions import HootenflatenExtensionManager
    if sys.argv[1] != 'createall':
        HootenflatenExtensionManager(app)
    manager.run()

