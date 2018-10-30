from DevPlugin import DevopsAppPlugin

class Log(DevopsAppPlugin):
    def __init__(self, app):
        super().__init__(app)

    def log(self, *a, **kwg):
        print(a, kwg)

def setup(app):
    log = Log(app)
    app.register_class('Log.instance', log)
    app.register_logging(log.log)
