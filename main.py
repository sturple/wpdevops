import os, pkgutil, sys, re
from functools import partial
from pluginbase import PluginBase
import tkinter as tk
from tkinter import ttk
import pprint

# For easier usage calculate the path relative to here.
here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)

# Setup a plugin base for "example.modules" and make sure to load
# all the default built-in plugins from the builtin_plugins folder.
plugin_base = PluginBase(package='main.plugins')


class DevopsApp(object):
    '''
    This is the class that handles the PluginBase
    '''
    #TODO: will need a way to run this in background mode.
    #TODO: add logic to autoload modules if not present ie git, pluginbase, ...
    content = None
    mainframe = None
    vscrollbar = None
    background = "#e9e9e9"
    action = None
    root = None
    version = None
    author = None

    def __init__(self):
        # Each application has a name
        self.data = {
            'menu' : {},
            'instance' : {},
            'config' : {},
            'add_action' : {},
            'logger' : {},
            'information' : {},
            'current_repo' : {},
            'themes' : {}
        }

        self.log = self.logger;
        self.source = plugin_base.make_plugin_source(searchpath=['./plugins'])

        # this is for the config, to load configurations first, before any setups of plugins.
        for plugin_name in self.source.list_plugins():
            plugin = self.source.load_plugin(plugin_name)
            try:
                plugin.register(self)
            except AttributeError:
                pass

        # this should be the business logic for most plugins.
        for plugin_name in self.source.list_plugins():
            plugin = self.source.load_plugin(plugin_name)
            try:
                active = self.get_data('config.plugin_%s.active'%plugin_name, True)
                if active or active == 'True' or active == 'true' or active == 'yes':
                    plugin.setup(self)
            except AttributeError:
                pass

        self.build_gui()
        self.run_application()


    def register_class(self, name, instance):
        self.data['instance'][name] = instance

    def register_logging(self, logger):
        self.log = logger

    def register_config(self, config):
        self.data['config'] = config

    def register_menu(self, name, fnct):
        self.data['menu'][name] = fnct

    def register_theme(self, name, register, apply):
        ''' registers themes '''
        #TODO: determine if there is a way for themes to be added together
        self.data['themes'][name] = {
            'register' : register,
            'apply' : apply
        }


    def get_data(self,namespace="", default=None):
        ''' This uses namespace to parse through config file ie config.Repos.plugins '''
        spaces = re.sub(r'\s', '', namespace).split('.');
        v = self.data
        for space in spaces:
            try:
                v = v.get(space,default)
            except AttributeError as e:
                pass
        return v

    def do_action(self, name, *a, **kwg):
        ''' hooks do_action if no hook, then do defaults or do nothing used with add_action.'''
        #TODO: add priority.
        #TODO: figure out multiple action hooks how it is going to work.

        found = False
        for key, action in self.data.get('add_action', {}).items():
            if key == name:
                return action(*a, **kwg)
        if found == False and kwg.get('default', False):
            default_call = kwg.get('default')
            return default_call(*a, **kwg)

    def add_action(self, name, fnct):
        ''' used to register add_action, when a do_fucntion is called, it will cycle through the add_action for matches '''
        self.data['add_action'][name] =  fnct

    def logger(self, *msgs, **kw):
        ''' default logger, if no logger plugin is used '''
        for msg in msgs:
            print(msg)

    def run_application(self):
        '''
        Sets ups menus
        Goes through the instances that have been registered, and looks for startup=True for render (summary)
        '''
        #pp = pprint.PrettyPrinter(indent=4, stream=sys.stderr)
        #pp.pprint(self.data)
        # render menus
        menubar = tk.Menu(self.root)
        for name, fnct in sorted(self.data.get('menu', {}).items()):
            fnct(menubar)
        self.root.config(menu=menubar)

        # render the startup
        for name, instance in sorted(self.data.get('instance',{}).items()):
            if instance.startup:
                self.render_plugin(instance)
        self.render()





    def render_plugin(self, instance):
        frame = self.create_frame()
        self.build_content(frame)
        instance.render(frame=frame)

    def build_gui(self):
        self.root = tk.Tk()
        for name, callbacks in sorted(self.data.get('themes', {}).items()):
            callbacks.get('register')()
        self.root.title("Devops")
        self.root.geometry("1500x900")
        self.vscrollbar = AutoScrollbar(self.root)
        self.vscrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        hscrollbar = AutoScrollbar(self.root, orient=tk.HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.content = tk.Canvas(self.root, yscrollcommand=self.vscrollbar.set, xscrollcommand=hscrollbar.set)
        self.content.config(bg=self.background)
        self.content.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.vscrollbar.config(command=self.content.yview)
        hscrollbar.config(command=self.content.xview)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.do_action('main_after_content', frame=self.root, row=10)

    def create_frame(self):
        self.content.delete('all')
        frame = tk.Frame(self.content)
        frame.config(bg=self.background, padx=12, pady=12)
        return frame

    def build_content(self, frame):
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
        self.content.create_window(0,0, window=frame, anchor=tk.N+tk.W)
        frame.update_idletasks()
        self.content.config(scrollregion=self.content.bbox("all"))
        return frame

    def render(self):
        self.root.mainloop()
        self.root.update()

    def set_attributes(self, **kwgs):
        self.version = kwgs.get('version')
        self.author = kwgs.get('author')


class AutoScrollbar(tk.Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise TclError("cannot use place with this widget")

def main():
    DevopsApp()

if __name__ == '__main__':
    print("You shouldn't run this program directly, please run wgui.py")
    exit()
