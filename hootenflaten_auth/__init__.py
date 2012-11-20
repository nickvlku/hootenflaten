__author__ = 'nick'

__meta__ = {
    'Author': 'Nick Vlku <nick@vlku.com>',
    'Title': 'Basic Authentication for Hootenflaten',
    'BlueprintName': 'hootenflaten_auth',
    'Version': 0.1,
    'Description': 'Allow users to login into your site',
    'ContextProcessors':  [
    ],
    'DefaultUrlPrefix': '/hootenflaten_auth',
    'NeedsConfiguration' : False
}

from flask.blueprints import Blueprint


from .views import hootenflaten_auth
