from Configurator.setting import Configuration, StringSetting, ListSetting, ComplexSetting

__author__ = 'nick'

class HootenflatenUserProfileConfig(Configuration):
    love_it = ListSetting(
        field =StringSetting(pretty_name="Field Wanted")
    )
    complicated_list = ListSetting(
        ComplexSetting(
            field_dict=dict(
                first_name = StringSetting(pretty_name="First Name"),
                Last_name = StringSetting(pretty_name="Last Name"),
            )
        )
    )
    complicated_test = ComplexSetting(
        field_dict=dict(
            full_name=StringSetting(pretty_name="Full Name"),
            some_value=StringSetting(pretty_name="Poop me", default_value="blah")
        )
    )
