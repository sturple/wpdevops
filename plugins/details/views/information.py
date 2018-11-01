from tkinter import ttk
from tkinter import *
import os, sys

def render_repository_info(self, frame):
    """
    This frame has information about the repositoryself.
    Includes the message dialog that has debug code and dirty files.
    """
    repo = self.repo
    repo_name = os.path.basename(os.path.normpath(repo.working_dir))

    version_frame = ttk.Frame(frame)
    ttk.Label(version_frame, text=self.get_data('current_repo.version')).pack(anchor="w",side="left")
    ttk.Button(version_frame, text="Change Version", command=lambda: self.action_change_version()).pack(anchor="w", side="right")

    status_color, _, _ = self.get_repo_health(repo_name, repo)
    status_canvas = Canvas(frame, width=32, height=32, bg=self.app.background, highlightthickness=0)
    status_canvas.create_oval(2,2,25,25, fill=status_color)

    components = [
        (ttk.Label(frame, text="Name"), ttk.Label(frame, text=repo_name)),
        (ttk.Label(frame, text="Active Branch"), ttk.Label(frame, text=repo.active_branch.name)),
        (ttk.Label(frame, text="Version File"), ttk.Label(frame, text=self.get_data('current_repo.version_file'))),
        (ttk.Label(frame, text="Version"), version_frame),
        (ttk.Label(frame, text="Latest Tag"), ttk.Label(frame, text=self.get_data('current_repo.latest_tag'))),
        (ttk.Label(frame, text="Health"), status_canvas),

    ]
    row = 100;
    for label, value in components:
        label.config(style="Bold.TLabel")
        label.grid(column=0, row=row, padx=4, pady=4, sticky=(W))
        value.grid(column=1, row=row, padx=4, pady=4, sticky=(W))
        row += 1

    #error frames
    error_frame = ttk.LabelFrame(frame, text="")
    self.render_repository_errors(error_frame)
    error_frame.grid(row=row, column=0,  columnspan=2, padx=8, pady=8, sticky=(W))
