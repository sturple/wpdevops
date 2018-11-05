#!/usr/bin/env python3
import sys, os, argparse

def setup(app):
    wp_plugin = WordPressPlugin(app)
    app.register_class('WordPressPlugin.instance', wp_plugin)

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append('%s/../../'%base_dir)
    sys.path.append('%s/../../plugins/config/'%base_dir)

    from push import Push
    from config import Config
    wp_plugin = WordPressPlugin(None)
    conf = Config(None)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--docs', help='Shows docs for this process', default='', nargs='?')
    args = parser.parse_args()
    docs = getattr(args,'docs')
    if docs or docs == None:
        help(WordPressPlugin)
    else:
        wordpress_plugin.term_plugin(conf.get_data())

else:
    from .wordpress_plugin import WordPressPlugin
