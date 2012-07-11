import importlib
from base.models import CustomQuestion

__author__ = 'nick'

from wtforms.form import Form

def custom_questions_form():
    fields_module = importlib.import_module("wtforms.fields")

    questions = CustomQuestion.query.order_by("position")
    attributes = {}
    for question in questions:
        field_type = fields_module.__getattribute__(question.widget)
        attributes[question.name] = field_type()
    new_cls = type('CustomQuestionForm', (Form,), attributes)

    return new_cls