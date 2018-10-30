from DevPlugin import DevopsAppPlugin
import tkinter as tk
from tkinter import scrolledtext as tkst

class Push(DevopsAppPlugin):
    commit_message = None
    synctoserver = None
    commit_version = None

    def __init__(self, app):
        super().__init__(app)
        self.name = 'push'


    def action_wpush(self):
        pass

    def render(self, *a, **kwg):
        pass

    def render_commit_message(self, *arg, **kwg):
        frame = kwg.get('frame', None)
        if frame != None:
            self.render_repository_actions(frame)

    def render_repository_actions(self, frame):
        """
        Gets the wpull and commit message
        """
        #self.synctoserver = tk.IntVar()
        self.commit_version = tk.IntVar()
        self.commit_message = tkst.ScrolledText(master=frame, wrap=tk.WORD, height=5, width=60)

        option_frame = tk.Frame(frame, background=self.app.background)

        if self.get_data('current_repo.version') == self.get_data('current_repo.latest_tag') and self.get_data('current_repo.version'):
            msg = "Version and latest git tag should not be the same for %s branch %s, please bump your version" %(self.get_data('current_repo.repo_name'), repo.active_branch.name )
            self.log(msg, level='warn')
        else:
            tk.Checkbutton(option_frame, text="Check to create %s version" %self.get_data('current_repo.version'), variable=self.commit_version , background=self.app.background).grid(row=0,column=0, sticky="w", padx=4)

        #tk.Checkbutton(option_frame, text="Sync to Server", variable=self.synctoserver, background=self.app.background).grid(row=1,column=0, sticky="w", padx=4)

        tk.Label(frame, text="Commit Message").grid(row=0, column=0, sticky="w")
        self.commit_message.grid(row=1, column=0, sticky="w",pady=4, padx=4)
        option_frame.grid(row=1, column=1, sticky="nw", padx=4, pady=4)
        tk.Button(frame, text="Push", command=lambda: self.action_wpush()).grid(row=100, column=0, sticky="w")



def setup(app):
    push = Push(app)
    app.register_class('Push.instance', push)
    app.add_action('details_push_commit', push.render_commit_message)
