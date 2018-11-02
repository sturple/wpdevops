#!/usr/bin/env python3
import sys, os, argparse

def setup(app):
    pull = Pull(app)
    app.register_class('Pull.instance', pull)
    app.add_action('details_pull_action', pull.get_button)
    app.add_action('page_header_after', pull.get_clone_button)


if __name__ == '__main__':
    print('Running Pull in terminal mode')
    base_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append('%s/../../'%base_dir)
    sys.path.append('%s/../../plugins/config/'%base_dir)

    from pull import Pull
    from config import Config
    pull = Pull(None)
    conf = Config(None)

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clone', help='Uses Git Clone to get repo', default='')

    args = parser.parse_args()
    clone = getattr(args, 'clone')
    if clone:
        pull.term_clone(conf.get_data(), clone)
    else:
        pull.term_pull(conf.get_data())
else:
    from .pull import Pull
