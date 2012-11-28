import importlib
from base.models import Extension

class HootenflatenExtensionManager(object):

    def __init__(self, app=None):
        self.app = app
        self.EXTENSIONS = {}
        self.EXTENSIONS_NEED_CONFIG = {}

        if app is not None:
            self.init_app(app)

    def context_processor(self):
        return dict(ExtensionManager=self)

    def init_app(self, app):
        self.app = app
        self.init_extensions()
        self.app.context_processor(self.context_processor)

    def get_extensions(self):
        return self.EXTENSIONS

    def get_extensions_needing_config(self):
        return self.EXTENSIONS_NEED_CONFIG

    def register(self,e):
        with self.app.app_context():
            ext = Extension.query.filter_by(extension_name=e.__meta__['BlueprintName']).first()

            if ext is None:
                ext = Extension()
                ext.extension_name = e.__meta__['BlueprintName']
                needs_config = e.__meta__.get('NeedsConfiguration', False)
                ext.needs_configuration = needs_config
                ext.version = e.__meta__.get('Version', '0.0')
                ext.has_configuration = False


                from base.database import db

                db.session.add(ext)
                db.session.commit()

            ext.package = e
            if ext.needs_configuration and not ext.has_configuration:
                self.app.logger.warn("%s needs configuration."  % e.__meta__.get('Title'))
                self.EXTENSIONS_NEED_CONFIG[ext.extension_name] = ext

            self.EXTENSIONS[e.__meta__["BlueprintName"]] = ext

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


            # Let's now import the config for the extension if it has config
            if ext.needs_configuration:
                config_class_name = ext.package.__meta__.get('ConfigClass', None)
                if config_class_name is not None:
                    module_name = ".".join(config_class_name.split(".")[:-1])
                    clazz_name = config_class_name.split(".")[-1]
                    config_mod = importlib.import_module(module_name)

                    ext.config = getattr(config_mod, clazz_name)

    def init_extensions(self):
        for extension in self.app.config['EXTENSIONS']:

            e = __import__(extension)
            blueprint = e.__dict__[e.__meta__['BlueprintName']]
            self.app.logger.info("Enabled Extension %s" % e.__meta__['Title'])
            self.app.register_blueprint(blueprint, url_prefix=e.__meta__['DefaultUrlPrefix'])
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