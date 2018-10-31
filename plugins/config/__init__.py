from .config import Config

def setup(app):
    config = Config(app)
    app.register_class('Config.instance', config)
    app.register_config(config.get_data() )
