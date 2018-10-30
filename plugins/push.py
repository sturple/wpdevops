from main import WpDevopsApp

class Push(WpDevopsApp):
    def __init__(self):
        super().__init__()

def setup(app):
    app.register_class('Push.instance', Push())
    print('setup push')
