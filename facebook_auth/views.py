import json
import urllib
import urlparse
import requests

from base import db
from site_configuration.themes import render

from flask import request, g, session, abort, current_app
from flask.ext.login import login_user, current_user
from flask_login import login_required

from facebook_auth import facebook_auth
from facebook_auth.models import FacebookUser
from facebook_auth.forms import FacebookRegistrationForm

@facebook_auth.route('/complete', methods=['GET'])
def bounceback_get():
    args = dict(client_id=current_app.config.get('FACEBOOK').get('ID'), redirect_uri=request.base_url)
    try:
        fb_verification_code =  request.args.get('code')
        args["client_secret"] = current_app.config.get('FACEBOOK').get('SECRET')
        args["code"] = fb_verification_code
    except Exception,e:
        current_app.logger.error("Error getting facebook verification code: %s" % (e))
        abort(500)

    try:
        access_token_request = "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args)
        page = requests.get(access_token_request).text
        response = urlparse.parse_qs(page)
        access_token = response["access_token"][-1]
        ac = str(access_token)
        current_app.logger.info("Got access token %s" % ac)
        detail_request = "https://graph.facebook.com/me?" + urllib.urlencode(dict(access_token=ac))
        detail_request_response = requests.get(detail_request).text
        user_details = json.loads(detail_request_response)
        auth = None
        if 'fb_auth' in session:
            # refresh the access token
            auth = FacebookUser.query.filter_by(id=session['fb_auth']).first()
            if auth is not None and auth.access_token != ac:
                auth.access_token = ac
                db.session.add(auth)
                db.session.commit()

        if auth is None:
            auth = FacebookUser.query.filter_by(facebook_id=user_details.get('id')).first()
            if auth is None:
                auth = FacebookUser(access_token = ac,
                                    first_name = user_details.get('first_name'),
                                    last_name = user_details.get('last_name'),
                                    facebook_id = user_details.get('id'),
                                    user_name = user_details.get('username'),
                                    email = user_details.get('email'))
                db.session.add(auth)
                db.session.commit()

        if auth.user is not None:
            g.user = auth.user
            login_user(auth.user, force=True)

        session['fb_auth'] = auth.id
        registration_form = FacebookRegistrationForm( first_name = auth.first_name,
                                        last_name = auth.last_name,
                                        email = auth.email )

        return render('facebook_auth/confirm_fb.html', facebook_user=auth, form=registration_form)

    except Exception, e:
        current_app.logger.exception("Error getting facebook access token: %s" % e)
        abort(500)

    return render('facebook_auth/confirm_fb.html')

@facebook_auth.route('/complete', methods=['POST'])
def complete():
    pass

@login_required
@facebook_auth.route('/test', methods=['GET'])
def test():
    return "Hello you are logged in! -- %s" % current_user.username