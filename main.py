import os, pkgutil
from functools import partial
from pluginbase import PluginBase
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import simpledialog, filedialog
from tkinter import scrolledtext as tkst

# For easier usage calculate the path relative to here.
here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)

# Setup a plugin base for "example.modules" and make sure to load
# all the default built-in plugins from the builtin_plugins folder.
plugin_base = PluginBase(package='main.plugins')


class DevopsApp(object):
    """Represents a simple example application."""

    content = None
    mainframe = None
    vscrollbar = None
    background = "#e9e9e9"
    action = None

    def __init__(self):
        # Each application has a name
        self.data = {
            'menu' : {},
            'instance' : {},
            'config' : {},
            'add_action' : {},
            'logger' : {},
            'information' : {},
            'current_repo' : {}
        }

        self.log = self.logger;
        self.source = plugin_base.make_plugin_source(searchpath=['./plugins'])

        for plugin_name in self.source.list_plugins():
            plugin = self.source.load_plugin(plugin_name)
            plugin.setup(self)

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

    def do_action(self, name, *a, **kwg):
        '''
        hooks do action if no hook, then do defaults.
        @todo add priority.
        @todo figure out multiple action hooks how it is going to work.
        '''
        found = False
        for key, action in self.data.get('add_action', {}).items():
            if key == name:
                return action(*a, **kwg)
        if found == False and kwg.get('default', False):
            default_call = kwg.get('default')
            return default_call(*a, **kwg)

    def add_action(self, name, fnct):
        self.data['add_action'][name] =  fnct

    def logger(self, *msgs, **kw):
        for msg in msgs:
            print(msg)

    def run_application(self):

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
    main()
