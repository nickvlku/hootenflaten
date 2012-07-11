__author__ = 'nick'

__meta__ = {
    'Author': 'Nick Vlku <nick@vlku.com',
    'Title': 'Facebook Authentication for Hootenflaten',
    'BlueprintName': 'fb_auth',
    'Version': 0.1,
    'Description': 'Allow users to login into the site via Facebook',
    'ContextProcessors':  [
        'facebook_auth.context_processors.inject_facebook_login'
    ],
    'DefaultUrlPrefix': '/facebook',
    'NeedsConfiguration' : True
}

from flask.blueprints import Blueprint


fb_auth = Blueprint('fb_auth', __name__, template_folder='templates')

from facebook_auth import views
from facebook_auth import models


