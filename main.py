import os, pkgutil
from functools import partial
from pluginbase import PluginBase


# For easier usage calculate the path relative to here.
here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)


# Setup a plugin base for "example.modules" and make sure to load
# all the default built-in plugins from the builtin_plugins folder.
plugin_base = PluginBase(package='main.plugins')


class DevopsApp(object):
    """Represents a simple example application."""

    def __init__(self):
        # Each application has a name

        self.menu = {}
        self.instance = {}
        self.source = plugin_base.make_plugin_source(searchpath=['./plugins'])

        for plugin_name in self.source.list_plugins():
            print(plugin_name)
            plugin = self.source.load_plugin(plugin_name)
            plugin.setup(self)

        self.run_application()

    def register_class(self, name, instance):
        self.instance[name] = instance


    def run_application(self):
        for name, instance in sorted(self.instance.items()):
            print(instance.get_value( 'myKey'))


class WpDevopsApp(object):
    def __init__(self):
        pass

    def get_value(self, key):
        return key, 'this is the value.'



def main():
    DevopsApp()

if __name__ == '__main__':
    main()
