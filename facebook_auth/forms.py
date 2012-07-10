__author__ = 'nick'

from flask.ext.wtf import Form, TextField, Required, Email
from flask.ext.wtf.html5 import EmailField

class FacebookRegistrationForm(Form):
    first_name = TextField("First Name", validators=[Required()])
    last_name = TextField("Last Name", validators=[Required()])
    email = EmailField("Email Address", validators=[Required(), Email()])

