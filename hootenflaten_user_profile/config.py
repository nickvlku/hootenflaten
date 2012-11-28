from Configurator.setting import Configuration, StringSetting

__author__ = 'nick'

class HootenflateUserProfileConfig(Configuration):
    fields_wanted = StringSetting(pretty_name="Fields Wanted")
