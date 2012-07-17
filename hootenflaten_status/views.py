from flask.helpers import jsonify
from base import db

from flask.globals import request
from flask_login import login_required, current_user

from hootenflaten_status import hootenflaten_status
from hootenflaten_status.models import StatusUpdate
from site_configuration.themes import render

@hootenflaten_status.route("/_post", methods=['GET'])
@login_required
def status_post():
    status_update = request.args.get('status')
    s = StatusUpdate()
    s.status_update = status_update
    s.user = current_user
    db.session.add(s)
    db.session.commit()

    return render("status.html", status=s)

@hootenflaten_status.route("/_awesome", methods=['GET'])
@login_required
def status_awesome():
    id = request.args.get('id')
    s = StatusUpdate.query.filter_by(id=id).first()
    if s is not None:
        if current_user in s.awesome_list:
            s.awesome_list.remove(current_user)
        else:
            s.awesome_list.append(current_user)
    db.session.add(s)
    db.session.commit()

    return s.to_json()

