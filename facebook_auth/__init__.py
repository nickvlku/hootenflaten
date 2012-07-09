from base import db, app
from base.models import Extension
from flask.blueprints import Blueprint

__author__ = 'nick'

__meta__ = {
    'Author': 'Nick Vlku <nick@vlku.com',
    'Title': 'Facebook Authentication for Hootenflaten',
    'BlueprintName': 'facebook_auth',
    'Version': 0.1,
    'Description': 'Allow users to login into the site via Facebook'
}

facebook_auth = Blueprint('facebook-auth', __name__, template_folder='templates')


def register(state):
    e = Extension.query.filter_by(extension_name=__meta__['BlueprintName']).first()
    if e is None:
        e = Extension()
        e.extension_name = __meta__['BlueprintName']
        e.configured = False
        state.app.logger.info("First run of %s.  Needs configuration."  % __meta__.get('Title'))
        db.session.add(e)
        db.session.commit()
    else:
        if not e.configured:
            state.app.logger.info("%s needs configuration."  % __meta__.get('Title'))


@app.context_processor
def inject_facebook_login_url():
    # TODO - If config is missing we need to log
    url = "https://graph.facebook.com/oauth/authorize?scope=%s&redirect_uri=%s&client_id=%s"\
    % (",".join(app.config.get('FACEBOOK', {}).get('SCOPES', None)),
       app.config.get('FACEBOOK', {}).get('REDIRECT_URI'),
       app.config.get('FACEBOOK', {}).get('ID'))
    return dict(facebook_url= url, facebook_enabled=True)

facebook_auth.record_once(register)

from facebook_auth import views
from facebook_auth import models

