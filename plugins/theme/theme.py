from DevPlugin import DevopsAppPlugin
from tkinter import ttk


class Theme(DevopsAppPlugin):
    title = ''
    location = None
    foreground = '#333333'
    background = '#e9e9e9'
    font ="Helvetica 11"
    bold_font ="Helvetica 11 bold"
    padding = 5

    def __init__(self, app):
        super().__init__(app)
        self.name = 'theme'



    def register(self):

        self.style = ttk.Style()
        self.style.theme_create('bcgov', parent="default")
        self.style.theme_use('bcgov')
        self.apply()

    def apply(self):
        self.style.theme_settings("bcgov", {
            "TLabel" : {
                "configure" : {
                    "padding" : self.padding,
                    "font" : self.font,
                    "foreground" : self.foreground,
                    "background" : self.background
                }
            },
            "Bold.TLabel" : {
                "configure" : {
                    "padding" : self.padding,
                    "font" : self.bold_font,
                    "foreground" : self.foreground,
                    "background" : self.background
                }
            },
            "TButton" : {
                "configure" : {
                    "padding" : self.padding,
                    "border" : self.padding,
                    "relief" : "ridge"
                },
                "map" : {
                    "foreground" : [('pressed','red'), ('active', 'blue')],
                    "background" : [('pressed', '!disabled','black'), ('active', 'white')]
                }
            },
            "TLabelFrame" : {
                "configure" : {
                    "padding" : self.padding,
                    "font" : self.font,
                    "foreground" : self.foreground,
                    "background" : self.background
                }            
            }
        })
