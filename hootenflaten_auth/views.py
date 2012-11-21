import datetime
from flask.ext.security.decorators import anonymous_user_required
from flask.ext.security.registerable import register_user
from flask.ext.security.utils import encrypt_password, get_post_login_redirect
from flask.ext.security.views import _ctx, _render_json
from flask_login import current_user
from flask_security import LoginForm
from werkzeug.datastructures import MultiDict
from werkzeug.local import LocalProxy

from base.database import db

from hootenflaten_auth.models import User

from flask import redirect, g, url_for, request, flash, current_app, after_this_request, Blueprint
from flask.ext.login import login_user

from site_configuration.themes import render

hootenflaten_auth = Blueprint('hootenflaten_auth', __name__, template_folder='templates')


_security = LocalProxy(lambda: current_app.extensions['security'])

_datastore = LocalProxy(lambda: _security.datastore)


@hootenflaten_auth.route("/register", methods=['GET'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('front_page'))
    from hootenflaten_auth.forms import RegistrationForm

    return render('register.html', form=RegistrationForm())

@hootenflaten_auth.route("/register", methods=['POST'])
def register_post():

    if current_user.is_authenticated():
        return redirect(url_for('front_page'))

    from hootenflaten_auth.forms import RegistrationForm

    form = RegistrationForm(request.form)
    if form.validate():
        user_dict = {
            "email": form.email.data,
            "password":  form.password.data

        }
        u = register_user(**user_dict)

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

def _commit(response=None):
    _datastore.commit()
    return response


@anonymous_user_required
@hootenflaten_auth.route("/login", methods=['GET', 'POST'], endpoint="login")
def login():
    """View function for login view"""


    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.user, remember=form.remember.data)
        after_this_request(_commit)

        if not request.json:
            return redirect(get_post_login_redirect())


    return render('login.html',
        login_user_form=form)


