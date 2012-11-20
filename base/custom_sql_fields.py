__author__ = 'nick'

from sqlalchemy import Column, DateTime, Integer, String

import sqlalchemy.types as types
import json

class ChoiceType(types.TypeDecorator):

    impl = types.VARCHAR(255)

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        try:
            return [k for k, v in self.choices.iteritems() if v == value][0]
        except:
            return None

    def process_result_value(self, value, dialect):
        try:
            return self.choices[value]
        except:
            return None


class JSONEncodedDict(types.TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage::

        JSONEncodedDict(255)

    """

    impl = types.VARCHAR(255)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
