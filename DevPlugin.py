class DevopsAppPlugin(object):
    def __init__(self, app):
        self.app = app
        pass

    def get_value(self, key):
        print(self.app)
        return key, 'this is the value.'
