from .summary import Summary

def setup(app):
    summary = Summary(app)
    app.register_class('Summary.instance', summary)
    app.register_menu('Summary.menu', summary.register_menus)
