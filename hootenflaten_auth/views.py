from flask.globals import request
from flask_security import User, LoginForm
from hootenflaten_auth import hootenflaten_auth
from hootenflaten_auth.forms import RegistrationForm
from site_configuration.themes import render

@hootenflaten_auth.route("/register", methods=['GET'])
def register():
    return render('register.html', form=RegistrationForm())

@hootenflaten_auth.route("/register", methods=['POST'])
def register_post():
    form = RegistrationForm(request.form)
    try:
        x = form.validate()
    except:
        return render('register.html', form=form)

    return "YAY!"

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