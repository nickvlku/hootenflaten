import importlib
from wtforms.validators import ValidationError

from base.models import CustomQuestion

from flask.ext.wtf import Form, TextField, Required, Email
from flask.ext.wtf.html5 import EmailField
from wtforms.fields.simple import PasswordField

__author__ = 'nick'

class PasswordMatch(Required):

    # a validator which makes a password field not validate if
    # another field is set and has not the same value

    def __init__(
            self,
            other_field_name,
            *args,
            **kwargs
    ):

        self.other_field_name = other_field_name
        super(PasswordMatch, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field.data != field.data:
            raise ValidationError('Passwords do not match')
        if other_field.data:
            super(PasswordMatch, self).__call__(form, field)

def custom_questions_form():

    def custom_fields(cls):
        fields = []
        for key in cls._fields.keys():
            if key.startswith("custom__"):
                attributes = key.split("__")
                fields.insert(int(attributes[1])-1, cls._fields.get(key))
        return fields

    fields_module = importlib.import_module("wtforms.fields")

    questions = CustomQuestion.query.order_by("position")
    attributes = dict()
    attributes['custom_fields'] = []
    number_of_fields = 0
    for question in questions:
        field_type = fields_module.__getattribute__(question.widget)
        x = field_type(question.question)
        attributes["custom__%s__%s" % (question.position, question.name)] = x
        attributes['custom_fields'].append(x)
        number_of_fields += 1

    attributes['custom_fields_count'] = number_of_fields
    attributes['custom_fields'] = custom_fields
    new_cls = type('CustomQuestionForm', (Form,), attributes)

    return new_cls
