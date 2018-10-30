from DevPlugin import DevopsAppPlugin

class Push(DevopsAppPlugin):
    def __init__(self, app):
        super().__init__(app)

def setup(app):
    app.register_class('Push.instance', Push(app))
    print('setup push')
