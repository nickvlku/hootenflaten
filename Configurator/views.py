from flask import render_template
from Configurator import configurator_app

@configurator_app.route('/test')
def test():
    return render_template("configurator/main.html")



