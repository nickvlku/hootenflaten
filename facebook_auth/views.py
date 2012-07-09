import urllib
import urlparse
import requests

from base import app

from flask import request
from flask.helpers import url_for
from facebook_auth import facebook_auth
from site_configuration.themes import render

@facebook_auth.route('/complete', methods=['GET'])
def bounceback_get():
    protocol = 'http://'
    if request.is_secure:
        protocol = 'https://'
    redir = request.base_url
    args = dict(client_id=app.config.get('FACEBOOK').get('ID'), redirect_uri=redir)
    try:
        fb_verification_code =  request.args.get('code')
        args["client_secret"] = app.config.get('FACEBOOK').get('SECRET')
        args["code"] = fb_verification_code
    except Exception,e:
        app.logger.error("Error getting facebook verification code: %s" % (e))
        #try to login the user
    try:
        access_token_request = "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args)
        page = requests.get(access_token_request).text
        response = urlparse.parse_qs(page)
        access_token = response["access_token"][-1]
        ac = str(access_token)
        app.logger.info("Got access token %s" % ac)


    except Exception, e:
        app.logger.error("Error getting facebook access token: %s" % (e))

    return render('facebook_auth/confirm_fb.html')

@facebook_auth.route('/complete', methods=['POST'])
def bounceback_post():
    pass

