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
        ''' This action is called from button on summary page '''

        self.repo = repo
        self.app.render_plugin(self)

    def action_change_version(self):
        self.log('change version', level="debug")


    def action_merge_branch(self, branch):
        self.log('merge branch', level="debug")


    def action_delete_branch(self, branch):
        """Deletes Branch in the repo info section.  This is only active, if branch is not selected"""
        if self.askyesno("Delete Branch","Are you sure you want to delete %s branch" %branch):
            self.repo.git.branch('-d', branch)
            self.log('Deleted %s branch' % branch, level='success')
            self.app.render_plugin(self)

    def action_switch_branch(self, branch):
        ''' Switches branches  and reloads page'''
        try:
            self.repo.git.checkout(branch)
            self.app.render_plugin(self)
        except git.GitCommandError as error:
            self.log(str(error), level='error')
            self.log('Could not switch branches', level="error")


    def render(self, *arg, **kwg):
        """ this gets called from the main application, not called directly use self.app.render_plugin to invoke this method """
        self.repo = self.get_repo(self.repo)
        #self.log(self.app.data,level="debug")
        frame = kwg.get('frame', None)
        if frame != None:
            self.app.action = self.name
            self.render_repository(frame)

    def add_repo_button(self, *arg, **kwg):
        """
        This is from a do_action summary_repo_name in the summary plugin
        it replaces a label with the button.
        """
        frame = kwg.get('frame', None)
        button = None
        repo = kwg.get('repo', None)
        if frame != None and repo != None:
            call = lambda repo=repo: self.action_repo_info(repo)
            button = ttk.Button(frame, text=kwg.get('repo_name', '??'), command=call  )
        return button

    def render_repository(self, frame):
        ''' This creates the frames for the repository Information '''
        self.set_page_header(frame, self)

        info_frame = ttk.LabelFrame(frame, text="Information")
        self.render_repository_info(info_frame)
        info_frame.grid(row=10, column=0, padx=8, pady=8, sticky="nw")

        branch_frame = ttk.LabelFrame(frame, text="Braches")
        self.render_branches(branch_frame)
        branch_frame.grid(row=10, column=1, padx=8, pady=8, sticky="nw")

        action_frame = ttk.LabelFrame(frame, text="Actions")
        self.app.do_action('details_push_commit', frame=action_frame, instance=self)
        action_frame.grid(row=11, column=0, padx=8, pady=8, sticky="nw")


    from .views.information import render_repository_info
    from .views.branches import render_branches
    from .views.errors import render_repository_errors
