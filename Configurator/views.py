from flask import render_template
from Configurator import configurator_app

@configurator_app.route('/test/<extension>')
def test(extension):
    from base.flask_extensions import hootenflaten_extension_manager
    e = hootenflaten_extension_manager.EXTENSIONS.get(extension,None)

    return render_template("configurator/main.html", extension=e)



