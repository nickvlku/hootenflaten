class ConfigurationSetting(object):
    def __init__(self, setting_name, required=False, default_value=None):
        self.required = required
        self.default_value = default_value
        self.value = None
        self.setting_name = setting_name
        self.extension = None

class StringSetting(ConfigurationSetting):
    pass

class ConfigurationBase(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(ConfigurationBase, cls).__new__
        config_fields = {
            '__fields__' : {},
            '__fields_values__' : {},
            '__extension__': None
        }
        attrs.update(config_fields)

        return super_new(cls, name, bases, attrs)

class Configuration(object):
    __metaclass__ = ConfigurationBase

    def __init__(self, *args, **kwargs):
        for attr_name, attr_value in self.__class__.__dict__.items():
            if not attr_name.startswith('_'):
                if isinstance(attr_value, ConfigurationSetting):
                    self.__fields__[attr_name] = attr_value
                    self.__field_values__[attr_name] = None

    def __setattr__(self, name, value, *args, **kwargs):
        if self.__fields__.has_key(name):
            return self.__fields__[name].set_value(self, value)
        else:
            return super(Configuration, self).__setattr__(name, value)


    def __getattribute__(self, name, *args, **kwargs):
        ret_val = super(Configuration,self).__getattribute__(name, *args, **kwargs)
        if isinstance(ret_val,ConfigurationSetting):
            if self.__fields__.has_key(name):
                return self.__fields__[name].get_value(self)
            else:
                return None
        else:
            return ret_val
