from .pipeline import Pipeline

def setup(app):
    pipeline = Pipeline(app)
    app.add_action('sync_to_server', pipeline.sync_to_server)
    app.add_action('push_successful', pipeline.push_successful)
    app.add_action('push_error', pipeline.push_error)
