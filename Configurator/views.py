from flask import render_template, redirect, url_for, request
from Configurator import configurator_app

@configurator_app.route('/settings/<extension>', methods=['GET'])
def extension_setting(extension):
    from base.flask_extensions import hootenflaten_extension_manager
    e = hootenflaten_extension_manager.EXTENSIONS.get(extension,None)
    meta_info = hootenflaten_extension_manager.EXTENSIONS_CLASS.get(extension, None)
    return render_template("configurator/main.html", extension=e, meta_info=meta_info)


@configurator_app.route('/settings/<extension>', methods=['POST'])
def extension_setting_post(extension):
    from base.flask_extensions import hootenflaten_extension_manager
    e = hootenflaten_extension_manager.EXTENSIONS.get(extension,None)
    config = e.config()
    for field in config.get_fields():
        if field in request.form:
            setattr(config, field, request.form.get(field))
    config.save()

    meta_info = hootenflaten_extension_manager.EXTENSIONS_CLASS.get(extension, None)
    return render_template("configurator/main.html", extension=e, meta_info=meta_info)
