from flask.helpers import jsonify
from base import db

from flask.globals import request
from flask_login import login_required, current_user
from base.models import Comment

from hootenflaten_status import hootenflaten_status
from hootenflaten_status.models import StatusUpdate
from site_configuration.themes import render

import uuid

@hootenflaten_status.route("/_post", methods=['GET'])
@login_required
def status_post():
    status_update = request.args.get('status')
    s = StatusUpdate()
    s.status_update = status_update
    s.user = current_user
    db.session.add(s)
    db.session.commit()
    db.session.flush()
    return render("hootenflaten_status/status.html", status=s)

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
    else:
        return jsonify()

@hootenflaten_status.route("/_delete", methods=['GET'])
@login_required
def status_delete():
    id = request.args.get('id')
    s = StatusUpdate.query.filter_by(id=id).first()
    if s is not None:
        if s.user == current_user:
            s.active = False
            db.session.add(s)
            db.session.commit()
            response = jsonify(status="SUCCESS")
            return response
        else:
            return jsonify(status="NOTAUTHORIZED")
    else:
        return jsonify(status="FAIL")

# this should be consolidated with status_delete at some point but
# HootenflatenBaseObject is not a db.Model so we can't query it.
@hootenflaten_status.route("/_comment/_delete", methods=['GET'])
@login_required
def status_comment_delete():
    id = request.args.get('id')
    c = Comment.query.filter_by(id=id).first()
    if c is not None:
        if c.user == current_user:
            c.active = False
            db.session.add(c)
            db.session.commit()
            response = jsonify(status="SUCCESS")
            return response
        else:
            return jsonify(status="NOTAUTHORIZED")
    else:
        return jsonify(status="FAIL")


@hootenflaten_status.route("/_comment/_awesome", methods=['GET'])
@login_required
def status_comment_awesome():
    id = request.args.get('id')
    c = Comment.query.filter_by(id=id).first()
    if c is not None:
        if current_user in c.awesome_list:
            c.awesome_list.remove(current_user)
        else:
            c.awesome_list.append(current_user)
        db.session.add(c)
        db.session.commit()

        return c.to_json()
    else:
        return jsonify()

@hootenflaten_status.route("/_comment", methods=['GET'])
@login_required
def status_comment():
    # TODO: Right now if you know the id of a status update and you have an account you can comment on it.
    # TODO: ie, there's no real privacy security around this

    id = request.args.get('id')
    s = StatusUpdate.query.filter_by(id=id).first()
    if s is not None:
        c = Comment()
        c.comment = request.args.get('comment')
        c.user = current_user
        db.session.add(c)

        s.comments.append(c)
        db.session.add(s)

        db.session.commit()

        return render("hootenflaten_status/comment.html", comment=c)
    else:
        return jsonify(status="FAIL")