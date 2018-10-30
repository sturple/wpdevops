from main import WpDevopsApp

class Pull(WpDevopsApp):
    def __init__(self):
        super().__init__()

def setup(app):
    app.register_class('Pull.instance', Pull())
    print('pull setup')
