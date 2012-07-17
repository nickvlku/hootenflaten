__author__ = 'nick'

from flask import current_app

def inject_facebook_login():
    # TODO - If config is missing we need to log
    url = "https://graph.facebook.com/oauth/authorize?scope=%s&redirect_uri=%s&client_id=%s"\
    % (",".join(current_app.config.get('FACEBOOK_SCOPES', [])),
       current_app.config.get('FACEBOOK_REDIRECT_URL', ''),
       current_app.config.get('FACEBOOK_ID'))
    return dict(facebook_url= url, facebook_enabled=True)
