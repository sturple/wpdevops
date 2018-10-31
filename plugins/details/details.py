from DevPlugin import DevopsAppPlugin
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as tkst
import os, sys

class Details(DevopsAppPlugin):
    repo = None
    def __init__(self, app):
        super().__init__(app)
        self.name = 'details'

    def action_repo_info(self, repo):
        self.repo = repo
        os.chdir(self.repo.working_dir)
        version, vfile = self.get_version(repo.working_dir)
        current_repo = {
            'version' : version,
            'version_file' : vfile,
            'latest_tag' : self.cmd(['git', 'describe', '--abbrev=0', '--tags']),
            'debug_code' : self.check_debug_code(),
            'repo'       : self.repo,
            'repo_name'  : os.path.basename(os.path.normpath(repo.working_dir))
        }
        self.app.data['current_repo'] = current_repo
        self.app.render_plugin(self)

    def action_change_version(self):
        self.log('change version', level="debug")


    def action_merge_branch(self, repo, branch):
        self.log('merge branch', level="debug")


    def action_delete_branch(self, repo, branch):
        self.log('delete branch', level="debug")

    def action_switch_branch(self, repo, branch):
        self.log('switch branch', level="debug")

    def render(self, *arg, **kwg):
        frame = kwg.get('frame', None)
        if frame != None:
            self.app.action = self.name
            self.render_repository(frame)

    def add_repo_button(self, *arg, **kwg):
        frame = kwg.get('frame', None)
        button = None
        repo = kwg.get('repo', None)
        if frame != None and repo != None:
            call = lambda repo=repo: self.action_repo_info(repo)
            button = ttk.Button(frame, text=kwg.get('repo_name', '??'), command=call  )
        return button

    def render_repository(self, frame):
        '''
        This creates the frames for the repository Information
        '''


        self.set_page_header(frame)
        #information
        info_frame = ttk.LabelFrame(frame, text="Information")
        self.log(info_frame.style(),level="debug")
        self.render_repository_info(info_frame)

        branch_frame = ttk.LabelFrame(frame, text="Braches")
        self.render_branches(branch_frame)

        #action frame
        action_frame = ttk.LabelFrame(frame, text="Actions")
        self.app.do_action('details_push_commit', frame=action_frame)
        #self.render_repository_actions(action_frame)

        info_frame.grid(row=10, column=0, padx=8, pady=8, sticky="nw")
        branch_frame.grid(row=10, column=1, padx=8, pady=8, sticky="nw")
        action_frame.grid(row=11, column=0, padx=8, pady=8, sticky="nw")

    from .views.information import render_repository_info
    from .views.branches import render_branches

    def render_repository_errors(self, frame):
        """
        Shows debug code, and dirty files.
        """
        repo = self.repo
        content_text = tkst.ScrolledText(master=frame, wrap=tk.WORD, height=8, width=120)
        content_text.configure(background="black", foreground="#cccccc")
        content_text.tag_config('untracked', foreground="red")
        content_text.tag_config('notstaged', foreground="orange")
        content_text.tag_config('staged', foreground="green")
        content_text.tag_config('title', font="Helvetica 14")
        debug_code = self.get_data('current_repo.debug_code')
        if debug_code != None and len(debug_code) > 5:
            content_text.insert("end", "Debug Code", 'title')
            content_text.insert("end", debug_code,'')

        staged_files = repo.git.status('--short', '-unormal')
        if repo.is_dirty() or len(repo.index.diff(None)) > 0 or len(staged_files) > 3:
            content_text.insert("end", "\n\nDirty Files", 'title')
            for untrack in repo.untracked_files:
                content_text.insert("end","\nuntracked - %s"%untrack,'untracked')

            for item in repo.index.diff(None):
                content_text.insert("end","\nnot staged - %s"%item.a_path,'notstaged')

            content_text.insert("end", "\n%s" %staged_files, 'staged')
        content_text.pack(fill=tk.BOTH, expand=True, anchor="w")
