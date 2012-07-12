from flask.ext.wtf import Form, TextField, Required, Email
from flask.ext.wtf.html5 import EmailField

from wtforms.fields.simple import PasswordField

from base.form_helpers import custom_questions_form, PasswordMatch

__author__ = 'nick'

class RegistrationForm(custom_questions_form()):
    first_name = TextField("First Name", validators=[Required()])
    last_name = TextField("Last Name", validators=[Required()])
    email = EmailField("Email Address", validators=[Required(), Email()])
    password = PasswordField("Password", validators=[Required()])
    confirm_password = PasswordField("Confirm Password", validators=[PasswordMatch('password', message='Passwords need to match')])

