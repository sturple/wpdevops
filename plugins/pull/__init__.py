from .pull import Pull

def setup(app):
    pull = Pull(app)
    app.register_class('Pull.instance', pull)
    app.add_action('details_pull_action', pull.get_button)
    app.add_action('page_header_after', pull.get_clone_button)
