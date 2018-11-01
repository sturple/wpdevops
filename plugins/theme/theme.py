from DevPlugin import DevopsAppPlugin
from tkinter import ttk


class Theme(DevopsAppPlugin):
    title = ''
    location = None
    foreground = '#333333'
    background = '#e9e9e9'
    font_size = 13
    font_family = 'Helvetica'

    padding = 5

    def __init__(self, app):
        super().__init__(app)
        self.name = 'theme'
        self.font ="%s %d" %(self.font_family, self.font_size)
        self.bold_font ="%s %d bold"  %(self.font_family, self.font_size)
        self.h1_font = "%s %d bold"  %(self.font_family, self.font_size)



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
            "Warn.TLabel" : {
                "configure" : {
                    "padding" : self.padding,
                    "font" : self.font,
                    "foreground" : "red",
                    "background" : self.background
                }
            },
            "H1.TLabel" : {
                "configure" : {
                    "padding" : self.padding,
                    "font" : self.h1_font,
                    "foreground" : self.foreground,
                    "background" : self.background
                }
            },
            "TButton" : {
                "configure" : {
                    "padding" : (20, 5, 20, 5),
                    "border" : 4,
                    "relief" : "ridge"
                },
                "map" : {
                    "foreground" : [('pressed','red'), ('active', 'blue')],
                    "background" : [('pressed', '!disabled','black'), ('active', 'white')]
                }
            },
            "TLabelframe" : {
                "configure" : {
                    "padding" : self.padding,
                    "font" : self.font,
                    "foreground" : self.foreground,
                    "background" : self.background,
                    "relief" : 'groove'
                }
            },
            "TCheckbutton" : {
                "configure" : {
                    "padding" : self.padding,
                    "font" : self.font,
                    "foreground" : self.foreground,
                    "background" : self.background
                }
            },
            "tixScrolledText" : {
                "configure" : {
                    "padding" : self.padding,
                    "font" : "Courier 16",
                    "foreground" : "#cccccc",
                    "background" : 'black'

                }
            }
        })
