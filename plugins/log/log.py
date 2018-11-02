from DevPlugin import DevopsAppPlugin
import pprint
import sys, re, os, inspect
from  tkinter import *
from tkinter import scrolledtext as tkst

class Log(DevopsAppPlugin):
    '''
    The Log Plugin is used for logging to the console, file, and graphically interfaces.
    '''
    #TODO: add logging to file
    #TODO: re do how logging items have a level.  Instead of using the fg class wrapped around text, make it an object, so it doesn't have to be parsed by gui.

    def __init__(self, app):
        super().__init__(app)
        self.name = 'log'

    def log(self, *msgs, **kwg):
        """ This is the logging function, adds color """
        #TODO: need to fix log(str1, str2, str3) --to show up on one line
        pp = pprint.PrettyPrinter(indent=4, stream=sys.stderr)

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

    def log_loop(self, template, *msgs, **kwg):
        pp = pprint.PrettyPrinter(indent=4, stream=sys.stderr)
        for msg in msgs:
            if kwg.get('level','') == 'debug':
                pp.pprint(msgs)
            else:
                print(template%msg)

    def inline_console(self, *arg, **kwg):
        ''' inserts the console at bottom of app '''
        frame = kwg.get('frame', None)
        row = kwg.get('row', 100)
        if frame != None:
            text_box = tkst.ScrolledText(master=frame, wrap=WORD, height=10, width=600)
            text_box.configure(background="black", foreground="#cccccc")
            text_box.grid(row=row, column=0, sticky=W)
            sys.stdout = StdRedirector(text_box)

            self.diagnostic_buttons(frame, row+1)

    def diagnostic_buttons(self, frame, row):
        diag_frame = Frame(frame)
        ttk.Button(diag_frame, text="Test Log Format", command=lambda: self.test()).pack(anchor=W, side=LEFT)
        ttk.Button(diag_frame, text="Code todo/fixme", command=lambda: self.code_todo()).pack(anchor=W, side=LEFT)
        ttk.Button(diag_frame, text="Code Docs", command=lambda: self.code_docs()).pack(anchor=W, side=LEFT)
        ttk.Button(diag_frame, text="Config", command=lambda: self.show_config()).pack(anchor=W, side=LEFT)
        diag_frame.grid(row=row,column=0,columnspan=2, sticky=W)

    def show_config(self):
        self.log('See log file for config.')
        self.log(self.app.data,level="debug")

    def code_todo(self):
        dir = os.path.dirname(inspect.getfile(DevopsAppPlugin)) +'/'
        self.log('See log file for full list in %s'%dir)
        output = self.cmd(['egrep','-rn', '--color', '--include=*.py','TODO|FIXME', dir])
        print(output, file=sys.stderr)

    def code_docs(self):
        self.log('See log file for docs.')
        print(help(DevopsAppPlugin), file=sys.stderr)


    def test(self):
        ''' Tests the logging level '''
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
        self.text_space.tag_config('error', foreground="red")
        self.text_space.tag_config('warn', foreground="orange")
        self.text_space.tag_config('success', foreground="green")
        self.text_space.tag_config('normal', foreground="#dddddd")

    def write(self, string):
        ''' writes to the scrolltext '''
        #TODO: need to remove the ascii character infront and behind in linux, ok in mac osx
        tag = 'normal'
        if re.match(r'.*\[31m', string) is not None:
            tag = 'error'
        elif re.match(r'.*\[32m', string) is not None:
            tag = 'success'
        elif re.match(r'.*\[33m', string) is not None:
            tag = 'warn'

        string = re.sub(r'\[\d{2}m', '', string).strip('')
        self.text_space.config(state=NORMAL, foreground="white")
        self.text_space.insert("end", string, tag)
        self.text_space.see("end")
        #self.text_space.config(state=DISABLED)

    def flush(self):
        pass
