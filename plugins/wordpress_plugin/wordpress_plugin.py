from DevPlugin import DevopsAppPlugin
from tkinter import ttk
import os

class WordPressPlugin(DevopsAppPlugin):
    '''
    Class WordPressPlugin
    ~~~~~~~~~~

    Creates a GUI and a terminal program to Wordpress Plugin creator
    * A symlink should be created ie ln -s ./plugins/wordpress_plugin/__init__.py /usr/local/bin/wplugin
    * Usage
        * terminal - shows these docs.      [Command] wpull -d, --docs
    '''
    repo = None
    parent_instance = None

    def __init__(self, app):
        ''' initializes super, and sets name to pull '''
        super().__init__(app)
        self.name = 'wordpress_plugin'

    def term_plugin(self, data):
        ''' Terminal [Wordpress Plugin creator]  '''

        self.term_show_title('BCGov Wordpress Plugin Creator')
        dirname = os.path.abspath('.')
        if self.term_question('some question: %s [(Y)es/(N)o] (y) '%dirname, 'y', case_sensitive=True) == 'y':
            pass
