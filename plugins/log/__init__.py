from .log import Log

def setup(app):
    log = Log(app)
    app.register_class('Log.instance', log)
    app.register_logging(log.log)
    app.add_action('main_after_content', log.inline_console)
