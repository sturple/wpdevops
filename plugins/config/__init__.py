from .config import Config

def register(app):
    config = Config(app)
    app.register_config(config.get_data() )
