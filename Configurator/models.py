from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ConfigurationSetting(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    extension = db.Column(db.String(255))
    key_name = db.Column(db.String(255))
    key_value = db.Column(db.String(255))
    default_set = db.Column(db.Boolean())
    field_set_on = db.Column(db.DateTime())
    field_set_by = db.Column(db.String(255))
