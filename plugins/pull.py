from DevPlugin import DevopsAppPlugin

class Pull(DevopsAppPlugin):
    def __init__(self, app):
        super().__init__(app)

def setup(app):
    app.register_class('Pull.instance', Pull(app))
    print('pull setup')
