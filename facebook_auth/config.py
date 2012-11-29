from Configurator.setting import Configuration, StringSetting

__author__ = 'nick'

class FacebookAuthConfig(Configuration):
    facebook_app_id = StringSetting(pretty_name="Facebook App ID", required=True)
    facebook_secret = StringSetting(pretty_name="Facebook Secret", required=True)
    bounce_back_url = StringSetting(default_value="/facebook_auth/login", pretty_name="Bounceback URL", required=True)

    class Meta:
        order = ['facebook_app_id', 'facebook_secret', 'bounce_back_url']