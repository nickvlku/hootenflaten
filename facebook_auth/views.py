import json
import urllib
import urlparse
import datetime
import requests

from base import db
from site_configuration.themes import render

from flask import request, g, session, abort, current_app, url_for, redirect, flash
from flask.ext.login import login_user, current_user
from flask.ext.security import user_datastore
from flask_login import login_required

from facebook_auth import fb_auth
from facebook_auth.models import FacebookUser
from hootenflaten_auth.forms import RegistrationForm

@fb_auth.route('/register', methods=['GET'])
def register_facebook_account():
    if current_user.is_authenticated():
        return redirect(url_for('front_page'))

    auth_id = session['fb_auth']
    auth = FacebookUser.query.filter_by(id=auth_id).first()
    registration_form = RegistrationForm( first_name = auth.first_name,
        last_name = auth.last_name,
        email = auth.email )

    return render('facebook_auth/confirm_fb.html', facebook_user=auth, form=registration_form)

@fb_auth.route('/register', methods=['POST'])
def register_facebook_account_post():
    if current_user.is_authenticated():
        return redirect(url_for('front_page'))

    registration_form = RegistrationForm(request.form)
    registration_form.validate()
    pw = registration_form.password.data

    u = user_datastore.create_user(
        username=registration_form.email.data,
        email=registration_form.email.data,
        password=registration_form.password.data,
        active=True)

    u.created_at=datetime.datetime.utcnow()
    u.modified_at=datetime.datetime.utcnow()

    u.first_name=registration_form.first_name.data
    u.last_name=registration_form.last_name.data
    u.ran_through_first_run_wizard=False
    custom_questions = dict()
    for c in registration_form.custom_fields():
        custom_questions[c.id] = c.data

    u.custom_questions_json = custom_questions
    auth = FacebookUser.query.filter_by(id=session['fb_auth']).first()

    u.profile_image = 'https://graph.facebook.com/%s/picture' % auth.facebook_id

    auth.user = u
    db.session.add(u)
    db.session.add(auth)
    db.session.commit()
    if auth.user is not None:
        g.user = auth.user
        login_user(auth.user, force=True)
        flash('You were successfully logged in')

    return redirect(url_for('front_page'))

@fb_auth.route('/complete', methods=['GET'])
def bounceback_get():
    args = dict(client_id=current_app.config.get('FACEBOOK_ID'), redirect_uri=request.base_url)
    try:
        fb_verification_code =  request.args.get('code')
        args["client_secret"] = current_app.config.get('FACEBOOK_SECRET')
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
            flash('You were successfully logged in')

            return redirect(url_for('front_page'))


        session['fb_auth'] = auth.id

        return redirect(url_for('.register_facebook_account'))

    except Exception, e:
        current_app.logger.exception("Error getting facebook access token: %s" % e)
        abort(500)

    return render('facebook_auth/confirm_fb.html')


@login_required
@fb_auth.route('/test', methods=['GET'])
def test():
    return "Hello you are logged in! -- %s" % current_user.username