import datetime
from flask import render_template

from Configurator.models import ConfigurationDatabaseSetting
from flask_login import current_user
from base.flask_extensions import hootenflaten_extension_manager

class ConfigurationSetting(object):
    def __init__(self, required=False, default_value=None, pretty_name=None):
        self.required = required
        self.default_value = default_value
        self.value = None
        self.extension = None
        self.value_set = False
        self.pretty_name = pretty_name
        self.name = None

    def get_field_template(self):
        return None

    def get_value(self):
        if self.value_set:
            return self.value
        else:
            return self.default_value

    def set_value(self, value):
        self.value_set = True
        self.value = value

    def to_html(self, name, html=None, template=None):
        if template is None:
            template = self.get_field_template()

        if template is None and html is None:
            html = '<label for="%s">%s</label><input type="text" name="%s" value="%s"/>'

        if self.value is not None:
            field = self.value
        else:
            if self.default_value is not None:
                field = self.default_value
            else:
                field = ""
        if self.pretty_name is not None:
            pretty_name = self.pretty_name
        else:
            pretty_name = name

        if template is not None:
            return template
        else:
            return html % (name, pretty_name, name, field)

class HootenflatenStyleConfigurationSetting(ConfigurationSetting):
    def get_field_template(self):

        return render_template("configurator/form_fields/%s.html" % self.__class__.__name__,
            pretty_name = self.pretty_name,
            form_field = self.name,
            value = self.get_value()
        )

class StringSetting(HootenflatenStyleConfigurationSetting):
    pass

class ListSetting(HootenflatenStyleConfigurationSetting):

    def __init__(self, field, required=False, default_value=None, pretty_name=None):
        super(ListSetting, self).__init__(required=required, default_value=default_value, pretty_name=pretty_name)
        self.field = field
        self.field_values = []

    def get_value(self):
        return self.field_values

    def add_value(self, field_value):
        new_field = self.field.__class__()
        new_field.set_value(field_value)
        self.field_values.append(new_field)

    def set_value(self, value):
        self.field_values = value

class ComplexSetting(HootenflatenStyleConfigurationSetting):
    def __init__(self, field_dict, required=False, default_value=None, pretty_name=None):
        super(ComplexSetting, self).__init__(required=required, default_value=default_value, pretty_name=pretty_name)
        self.field_dict = field_dict

    def get_value(self):
        return self.field_dict

    def get_specific_value(self, key):
        value = self.field_dict.get(key,None)
        return value.get_value()

    def set_value(self, field_dict):
        self.field_dict = field_dict

    def set_specific_value(self, key, value):
        field = self.field_dict.get(key)
        field.set_value(value)


class ConfigurationBase(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(ConfigurationBase, cls).__new__
        config_fields = {
            '__field_order__' : [],
            '__fields__' : {},
            '__field_values__' : {},
            '__field_to_config_objs__': {},
            '__extension__': None
        }
        attrs.update(config_fields)

        return super_new(cls, name, bases, attrs)

class Configuration(object):
    __metaclass__ = ConfigurationBase

    def __init__(self, *args, **kwargs):
        self.__extension__ = self.__module__.split(".")[0]
        order_explicit = False
        self.__field_order__ = []
        self.__fields__ = {}
        self.__field_values__ = {}
        self.__field_to_config_objs__ = {}

        if 'Meta' in self.__class__.__dict__:
            meta_attr = getattr(self.__class__, 'Meta')
            if hasattr(meta_attr, 'order'):
                self.__field_order__ = getattr(meta_attr,'order')
                order_explicit = True

        for attr_name, attr_value in self.__class__.__dict__.items():

            if not attr_name.startswith('_'):
                if isinstance(attr_value, ConfigurationSetting):
                    attr_value.name = attr_name

                    # first we check if there are corresponding values in the database
                    config = ConfigurationDatabaseSetting.query.filter_by(extension=self.__extension__, key_name=attr_name).first()

                    if config is not None:
                        self.__fields__[attr_name] = attr_value
                        self.__fields__[attr_name].set_value(config.key_value)
                        self.__field_to_config_objs__[attr_name] = config
                        self.__field_values__[attr_name] = config.key_value
                    else:
                        # if not we initialize via default values
                        self.__fields__[attr_name] = attr_value
                        default_value = self.__fields__[attr_name].default_value
                        self.__field_values__[attr_name] = default_value

                    if not order_explicit:
                        self.__field_order__.append(attr_name)

                elif attr_name == 'Meta':
                    if hasattr(attr_value, 'order'):
                        self.__field_order__ = getattr(attr_value,'order')

    def __setattr__(self, name, value, *args, **kwargs):
        if self.__fields__.has_key(name):
            v = self.__fields__[name].set_value(value)
            self.__field_values__[name] = value
            return v
        else:
            return super(Configuration, self).__setattr__(name, value)


    def __getattribute__(self, name, *args, **kwargs):
        ret_val = super(Configuration,self).__getattribute__(name, *args, **kwargs)
        if isinstance(ret_val,ConfigurationSetting):
            if self.__fields__.has_key(name):
                return self.__fields__[name]
            else:
                return None
        else:
            return ret_val

    def field_to_html(self, field_name, html=None, template=None):
        actual_field = self.__fields__.get(field_name)
        return actual_field.to_html(field_name, html=template, template=template)

    def save(self):
        from base.database import db

        for value in self.__field_values__:
            if value in self.__field_to_config_objs__:
                c = self.__field_to_config_objs__.get(value)
            else:
                c = ConfigurationDatabaseSetting()
            c.extension = self.__extension__
            c.key_name = value
            c.key_value = self.__field_values__.get(value)
            c.default_set = False # has to change
            c.field_set_on = datetime.datetime.utcnow()
            try:
                c.field_set_by = current_user.id
            except:
                pass

            db.session.add(c)
            self.__field_to_config_objs__[value] = c

        e = hootenflaten_extension_manager.EXTENSIONS.get(self.__extension__)
        if not e.has_configuration:
            e.has_configuration = True
            db.session.add(e)

        db.session.commit()

    def get_fields(self):
        print self.__field_order__
        return self.__field_order__


class TestConfiguration(Configuration):
    full_name = StringSetting()

class AnotherTest(Configuration):
    full_name = StringSetting()
    bar_bar = StringSetting()