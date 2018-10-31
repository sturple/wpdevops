from .details import Details

def setup(app):
    details = Details(app)
    app.register_class('Details.instance', details)
    app.add_action('summary_repo_name', details.add_repo_button)
