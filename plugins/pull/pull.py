from DevPlugin import DevopsAppPlugin
from tkinter import ttk

class Pull(DevopsAppPlugin):
    def __init__(self, app):
        super().__init__(app)
        self.name = 'pull'

    def action_pull(self, repo):
        self.log('pull', repo, level="debug")

    def get_button(self, *arg, **kwgs):
        frame = kwgs.get('frame', None)
        repo = kwgs.get('repo', None)
        row = kwgs.get('row', 100)
        if frame != None and repo != None:
            ttk.Button(frame, text="Pull", command=lambda: self.action_pull(repo)).grid(column=0, row=row, padx=4, pady=4, sticky="w")
