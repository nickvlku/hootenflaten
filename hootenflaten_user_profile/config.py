from Configurator.setting import Configuration, StringSetting, ListSetting, ComplexSetting

__author__ = 'nick'

class HootenflatenUserProfileConfig(Configuration):
    profile_fields = ListSetting(
        field=StringSetting(pretty_name="Field Wanted")
    )
    complicated_test = ComplexSetting(
        field_dict=dict(
            full_name=StringSetting(pretty_name="Full Name"),
            some_value=StringSetting(pretty_name="Poop me", default_value="blah")
        )
    )
