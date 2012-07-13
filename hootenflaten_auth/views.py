import datetime
from flask_security import LoginForm

from base import db

from flask import redirect, g, url_for, request, flash
from flask.ext.login import login_user
from flask.ext.security import user_datastore, User

from site_configuration.themes import render

from hootenflaten_auth import hootenflaten_auth
from hootenflaten_auth.forms import RegistrationForm

@hootenflaten_auth.route("/register", methods=['GET'])
def register():
    return render('register.html', form=RegistrationForm())

@hootenflaten_auth.route("/register", methods=['POST'])
def register_post():
    form = RegistrationForm(request.form)
    if form.validate():
        u = user_datastore.create_user(
            username=form.email.data,
            email=form.email.data,
            password=form.password.data,
            active=True)

        u.created_at=datetime.datetime.utcnow()
        u.modified_at=datetime.datetime.utcnow()

        u.first_name=form.first_name.data
        u.last_name=form.last_name.data
        u.ran_through_first_run_wizard=False
        custom_questions = dict()
        for c in form.custom_fields():
            custom_questions[c.id] = c.data

        u.custom_questions_json = custom_questions
        db.session.add(u)
        db.session.commit()
        g.user = u
        login_user(u, force=True)
        flash('You were successfully logged in')

        return redirect(url_for('front_page'))

    else:
        return render('register.html', form=form)


@hootenflaten_auth.route("/email")
def username_valid():
    email = request.args.get('email', None)
    if email is None:
        return "false"
    user = User.query.filter_by(email=email).first()
    if user is None:
        return "true"
    else:
        return "false"

@hootenflaten_auth.route("/login")
def login():
    l = LoginForm()
    return render('login.html', form=LoginForm())