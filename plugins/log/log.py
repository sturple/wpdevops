from DevPlugin import DevopsAppPlugin
import pprint
import sys, re
import tkinter as tk
from tkinter import scrolledtext as tkst

class Log(DevopsAppPlugin):
    def __init__(self, app):
        super().__init__(app)
        self.name = 'log'

    def log(self, *msgs, **kwg):
        """ This is the logging function, adds color """
        pp = pprint.PrettyPrinter(indent=4, stream=sys.stderr)
        #msg = str(msg)
        out = ''

        if kwg.get('level','') == 'error':
            #self.log_loop(fg.RED + 'ERROR: %s' + fg.RESET, a, file=sys.stderr)
            self.log_loop(fg.RED + 'ERROR: %s'+ fg.RESET, msgs)
        elif kwg.get('level','') == 'warn':
            self.log_loop(fg.YELLOW + 'WARN:  %s'+ fg.RESET, msgs)
        elif kwg.get('level','') == 'debug':
            self.log_loop('%s', msgs, level="debug")
        elif kwg.get('level','') == 'success':
            self.log_loop(fg.GREEN + '%s' + fg.RESET, msgs)
        else:
            self.log_loop(fg.WHITE + '%s' + fg.RESET, msgs)

    def log_loop(self, template, msgs, **kwg):
        pp = pprint.PrettyPrinter(indent=4, stream=sys.stderr)
        for msg in msgs:
            if kwg.get('level','') == 'debug':
                pp.pprint(msg)
            else:
                print(template%msg)

    def inline_console(self, *arg, **kwg):
        frame = kwg.get('frame', None)
        row = kwg.get('row', 100)
        if frame != None:
            text_box = tkst.ScrolledText(master=frame, wrap=tk.WORD, height=10, width=600)
            text_box.grid(row=row, column=0, sticky=tk.W)
            sys.stdout = StdRedirector(text_box)

    def test(self):
        self.app.log('This is a single success', level="success")
        self.app.log('This is a normal', 'It also has multiple values', 'third')
        self.app.log('This is a warning', level="warn")
        self.app.log('This is an error', level="error")
        self.app.log('This is debug', 'Two lines for debug', level="debug")

class fg:
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE    = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'
    RESET   = '\033[39m'

class StdRedirector(object):
    """
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    """
    def __init__(self, text_widget):
        self.text_space = text_widget
        self.text_space.config(background="black", font="Courier 16")
        self.text_space.tag_config('error', foreground="red")
        self.text_space.tag_config('warn', foreground="orange")
        self.text_space.tag_config('success', foreground="green")
        self.text_space.tag_config('normal', foreground="#dddddd")

    def write(self, string):

        tag = 'normal'
        if re.match(r'.*\[31m', string) is not None:
            tag = 'error'
        elif re.match(r'.*\[32m', string) is not None:
            tag = 'success'
        elif re.match(r'.*\[33m', string) is not None:
            tag = 'warn'

        string = re.sub(r'\[\d{2}m', '', string)
        self.text_space.config(state=tk.NORMAL, foreground="white")
        self.text_space.insert("end", string, tag)
        self.text_space.see("end")
        #self.text_space.config(state=tk.DISABLED)

    def flush(self):
        pass
