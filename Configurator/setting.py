import datetime
from Configurator.models import ConfigurationDatabaseSetting
from flask_login import current_user

class ConfigurationSetting(object):
    def __init__(self, required=False, default_value=None):
        self.required = required
        self.default_value = default_value
        self.value = None
        self.extension = None
        self.value_set = False

    def get_value(self):
        if self.value_set:
            return self.value
        else:
            return self.default_value

    def set_value(self, value):
        self.value_set = True
        self.value = value

class StringSetting(ConfigurationSetting):
    pass

class ConfigurationBase(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(ConfigurationBase, cls).__new__
        config_fields = {
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
        for attr_name, attr_value in self.__class__.__dict__.items():
            if not attr_name.startswith('_'):
                if isinstance(attr_value, ConfigurationSetting):
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
                return self.__fields__[name].get_value()
            else:
                return None
        else:
            return ret_val

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

        db.session.commit()


class TestConfiguration(Configuration):
    full_name = StringSetting()

class AnotherTest(Configuration):
    full_name = StringSetting()
    bar_bar = StringSetting()