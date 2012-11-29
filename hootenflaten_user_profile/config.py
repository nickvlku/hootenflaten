from Configurator.setting import Configuration, StringSetting, ListSetting

__author__ = 'nick'

class HootenflatenUserProfileConfig(Configuration):
    profile_fields = ListSetting(
        field=StringSetting(pretty_name="Field Wanted")
    )
