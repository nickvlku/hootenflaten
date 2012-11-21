__author__ = 'nick'

__meta__ = {
    'Author': 'Nick Vlku <nick@vlku.com>',
    'Title': 'Basic Status Updates for Hootenflaten',
    'BlueprintName': 'hootenflaten_status',
    'Version': 0.1,
    'Description': 'Allow status updates on your site',
    'ContextProcessors':  [
    ],
    'DefaultUrlPrefix': '/status',
    'NeedsConfiguration' : False
}

from .views import hootenflaten_status



