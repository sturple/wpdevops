from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext as tkst

def render_repository_actions(self, frame):
    ''' Gets the wpull and commit message '''
    repo = self.get_data('current_repo.repo', {})
    self.synctoserver = IntVar()
    self.commit_version = IntVar()

    self.commit_message_component = tkst.ScrolledText(master=frame, wrap=WORD, height=5, width=60)

    option_frame = Frame(frame, background=self.app.background)
    if self.get_data('current_repo.version') == self.get_data('current_repo.latest_tag') and self.get_data('current_repo.version'):
        msg = "Version and latest git tag should not be the same for %s branch %s, please bump your version" %(self.get_data('current_repo.repo_name'), repo.active_branch.name )
        self.log(msg, level='warn')
    else:
        text = "Check to create %s version" %self.get_data('current_repo.version')
        Checkbutton(option_frame, text=text, variable=self.commit_version).grid(row=0,column=0, sticky=W, padx=4)

    Checkbutton(option_frame, text="Sync to Server", variable=self.synctoserver).grid(row=1,column=0, sticky=W, padx=4)

    ttk.Label(frame, text="Commit Message").grid(row=0, column=0, sticky="w")
    self.commit_message_component.grid(row=1, column=0, sticky="w",pady=4, padx=4)
    option_frame.grid(row=1, column=1, sticky="nw", padx=4, pady=4)
    ttk.Button(frame, text="Push", command=lambda: self.action_push()).grid(row=100, column=0, sticky="w")
