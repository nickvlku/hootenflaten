__author__ = 'nick'

from flask import current_app

def inject_facebook_login():
    # TODO - If config is missing we need to log
    url = "https://graph.facebook.com/oauth/authorize?scope=%s&redirect_uri=%s&client_id=%s"\
    % (",".join(current_app.config.get('FACEBOOK', {}).get('SCOPES', None)),
       current_app.config.get('FACEBOOK', {}).get('REDIRECT_URI'),
       current_app.config.get('FACEBOOK', {}).get('ID'))
    return dict(facebook_url= url, facebook_enabled=True)
