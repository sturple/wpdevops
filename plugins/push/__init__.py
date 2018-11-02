#!/usr/bin/env python3
import sys, os

def setup(app):
    push = Push(app)
    app.register_class('Push.instance', push)
    app.add_action('details_push_commit', push.render_commit_message)


if __name__ == '__main__':
    print('Running Push in terminal mode')
    sys.path.append('%s/../../'%os.getcwd())
    from push import Push
    push = Push(None)
else:
    from .push import Push
