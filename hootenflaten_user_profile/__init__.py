__author__ = 'nick'

__meta__ = {
    'Author': 'Nick Vlku <nick@vlku.com>',
    'Title': 'Basic User Profiles for Hootenflaten',
    'BlueprintName': 'hootenflaten_user_profile',
    'Version': 0.1,
    'Description': 'User profiles for Hootenflaten',
    'ContextProcessors':  [
    ],
    'DefaultUrlPrefix': '/profile',
    'NeedsConfiguration' : True,
    'DependsOn': [ 'hootenflaten_auth', ],
    'ConfigClass': 'hootenflaten_user_profile.config.HootenflateUserProfileConfig'

}

from flask.blueprints import Blueprint


hootenflaten_user_profile = Blueprint(__meta__['BlueprintName'], __name__, template_folder='templates')

from hootenflaten_user_profile import views
from hootenflaten_user_profile import models


