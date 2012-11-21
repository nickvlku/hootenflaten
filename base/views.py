from flask_login import login_required, current_user
from flask import redirect, url_for
from flask import Blueprint
from site_configuration.themes import render

root_views = Blueprint('root_views', __name__)

@root_views.route("/", )
def front_page():
    if current_user.is_authenticated():
        return redirect(url_for('.main'))
    return render('base.html')

@root_views.route('/main')
@login_required
def main():
    # TODO: Abstract out things that need to be on the front page from apps
    # TODO: We now get ALL status updates, we have to cross this against friend lists (or make this a configable option)
    from hootenflaten_status.models import StatusUpdate

    statuses = StatusUpdate.query.filter_by(active=True).order_by('-created_at').limit(100)
    return render("logged_in_base.html", statuses=statuses)

@root_views.route("/login")
def login():
    return redirect(url_for('hootenflaten_auth.login'))