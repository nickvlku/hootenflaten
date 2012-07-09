EXTENSIONS = {}

def init_extensions(app):
    for extension in app.config['EXTENSIONS']:
        e = __import__(extension)
        blueprint = e.__dict__[e.__meta__['BlueprintName']]
        app.logger.info("Enabled Extension %s" % e.__meta__['Title'])
        app.register_blueprint(blueprint, url_prefix="/facebook")