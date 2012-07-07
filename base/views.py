from base import app
from flask import render_template
from flask.ext.security import LoginForm, user_datastore
from site_configuration.themes import render

@app.route("/login")
def login():
    return render('login.html', form=LoginForm())

@app.route("/")
def front_page():
    return render('base.html')
