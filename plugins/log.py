from main import WpDevopsApp

class Log(WpDevopsApp):
    def __init__(self):
        super().__init__()

def setup(app):
    app.register_class('Log.instance', Log())
    print('Log setup')
