__author__ = 'nick'

__meta__ = {
    'Author': 'Nick Vlku <nick@vlku.com>',
    'Title': 'Facebook Authentication for Hootenflaten',
    'BlueprintName': 'fb_auth',
    'Version': 0.1,
    'Description': 'Allow users to login into the site via Facebook',
    'ContextProcessors':  [
        'facebook_auth.context_processors.inject_facebook_login'
    ],
    'DefaultUrlPrefix': '/facebook',
    'NeedsConfiguration' : True,
    'DependsOn': [ 'hootenflaten_auth', ],
    'ConfigClass': 'facebook_auth.config.FacebookAuthConfig'

}

from .views import fb_auth

