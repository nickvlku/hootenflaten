import importlib
from flask.blueprints import Blueprint

EXTENSIONS = {}

def register(e):
    from base.models import Extension
    from base import db, app

    ext = Extension.query.filter_by(extension_name=e.__meta__['BlueprintName']).first()
    if ext is None:
        ext = Extension()
        ext.extension_name = e.__meta__['BlueprintName']
        needs_config = e.__meta__.get('NeedsConfiguration', False)
        ext.configured = not needs_config
        ext.version = e.__meta__.get('Version', '0.0')
        if ext.configured:
            if needs_config:
                app.logger.warn("First run of %s.  Needs configuration."  % e.__meta__.get('Title'))
        db.session.add(ext)
        db.session.commit()
    else:
        if not ext.configured:
            app.logger.warn("%s needs configuration."  % e.__meta__.get('Title'))

def init_extensions(app):
    for extension in app.config['EXTENSIONS']:

        e = __import__(extension)
        blueprint = e.__dict__[e.__meta__['BlueprintName']]
        app.logger.info("Enabled Extension %s" % e.__meta__['Title'])
        app.register_blueprint(blueprint, url_prefix=e.__meta__['DefaultUrlPrefix'])
        EXTENSIONS[e.__meta__["BlueprintName"]] = e
        register(e)

        context_processors = e.__meta__.get('ContextProcessors', [])
        for context_processor in context_processors:
            try:
                module_name = ".".join(context_processor.split(".")[:-1])

                function = context_processor.split(".")[-1]
                mod = importlib.import_module(module_name)
                app.context_processor(getattr(mod, function))
            except:
                app.logger.exception("Error loading context processor %s" % context_processor)