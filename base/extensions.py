import importlib
from base.models import Extension

class HootenflatenExtensionManager(object):

    def __init__(self, app=None):
        self.app = app
        self.EXTENSIONS = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.init_extensions()

    def register(self,e):
        with self.app.app_context():
            ext = Extension.query.filter_by(extension_name=e.__meta__['BlueprintName']).first()

            if ext is None:
                ext = Extension()
                ext.extension_name = e.__meta__['BlueprintName']
                needs_config = e.__meta__.get('NeedsConfiguration', False)
                ext.configured = not needs_config
                ext.version = e.__meta__.get('Version', '0.0')
                if ext.configured:
                    if needs_config:
                        self.app.logger.warn("First run of %s.  Needs configuration."  % e.__meta__.get('Title'))



                from base.flask_extensions import db

                db.session.add(ext)
                db.session.commit()
            else:
                if not ext.configured:
                    self.app.logger.warn("%s needs configuration."  % e.__meta__.get('Title'))

            # let's import the models now so we can create them if they are there
            try:
                mod_name = "%s.%s" % (ext.extension_name, e.__meta__['BlueprintName'])
                mod = importlib.import_module(mod_name)
            except:
                self.app.logger.warn("%s has no models yo."  % e.__meta__.get('Title'))
                # no models in this extension!
                pass

            try:
                mod_name = "%s.%s" % (ext.extension_name, "views")
                mod = importlib.import_module(mod_name)
                self.app.logger.warn("%s has views yo."  % e.__meta__.get('Title'))
            except:
                self.app.logger.warn("%s has no views yo."  % e.__meta__.get('Title'))
                # no models in this extension!
                pass


    def init_extensions(self):
        for extension in self.app.config['EXTENSIONS']:

            e = __import__(extension)
            blueprint = e.__dict__[e.__meta__['BlueprintName']]
            self.app.logger.info("Enabled Extension %s" % e.__meta__['Title'])
            self.app.register_blueprint(blueprint, url_prefix=e.__meta__['DefaultUrlPrefix'])
            self.EXTENSIONS[e.__meta__["BlueprintName"]] = e
            self.register(e)


            context_processors = e.__meta__.get('ContextProcessors', [])
            for context_processor in context_processors:
                try:
                    module_name = ".".join(context_processor.split(".")[:-1])

                    function = context_processor.split(".")[-1]
                    mod = importlib.import_module(module_name)

                    self.app.context_processor(getattr(mod, function))
                except:
                    self.app.logger.exception("Error loading context processor %s" % context_processor)