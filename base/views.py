from flask_login import login_required, current_user
from flask import redirect, url_for
from base import app
from site_configuration.themes import render

@app.route("/")
def front_page():
    if current_user.is_authenticated():
        return redirect(url_for('main'))
    return render('base.html')

@login_required
@app.route('/main')
def main():
    return render("logged_in_base.html")