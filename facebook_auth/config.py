from Configurator.setting import Configuration, StringSetting

__author__ = 'nick'

class FacebookAuthConfig(Configuration):
    access_token = StringSetting()
    bounce_back_url =  StringSetting(default_value="/facebook_auth/login")