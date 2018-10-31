from .push import Push

def setup(app):
    push = Push(app)
    app.register_class('Push.instance', push)
    app.add_action('details_push_commit', push.render_commit_message)
