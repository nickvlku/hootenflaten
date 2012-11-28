from flask import render_template
from Configurator import configurator_app

@configurator_app.route('/test/<extension>')
def test(extension):


    return render_template("configurator/main.html", extension=e)



