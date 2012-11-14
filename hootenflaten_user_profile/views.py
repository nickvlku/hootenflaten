from flask.ext.login import login_required, current_user
from base import User
from hootenflaten_user_profile import hootenflaten_user_profile
from site_configuration.themes import render

@hootenflaten_user_profile.route("/<int:user_id>", methods=['GET'])
@login_required
def user_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render('hootenflaten_user_profile/main.html',
        profile_user=user)


@hootenflaten_user_profile.route("/", methods=['GET'])
@login_required
def user_profile_me():
    return user_profile(current_user.id)
