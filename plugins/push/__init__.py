#!/usr/bin/env python3
import sys, os, argparse

def setup(app):
    push = Push(app)
    app.register_class('Push.instance', push)
    app.add_action('details_push_commit', push.render_commit_message)


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append('%s/../../'%base_dir)
    sys.path.append('%s/../../plugins/config/'%base_dir)

    from push import Push
    from config import Config
    push = Push(None)
    conf = Config(None)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--docs', help='Shows docs for this process', default='', nargs='?')
    args = parser.parse_args()
    docs = getattr(args,'docs')
    if docs or docs == None:
        help(Push)
    else:
        push.term_push(conf.get_data())

else:
    from .push import Push
    
