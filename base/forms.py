import importlib
from base.models import CustomQuestion

__author__ = 'nick'

from wtforms.form import Form

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