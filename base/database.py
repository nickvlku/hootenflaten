from flask.ext.sqlalchemy import SQLAlchemy

db = None

def init_db(app):
    global db
    db = SQLAlchemy(app)