from DevPlugin import DevopsAppPlugin
import tkinter as tk
from tkinter import ttk
from git import Repo
import git
import os, sys

class Summary(DevopsAppPlugin):
    title = ''
    location = None

    def __init__(self, app):
        super().__init__(app)
        self.name = 'summary'
        self.startup = True

    def render(self, *a, **kwg):
        if self.location == None:
            for title, location in self.app.data.get('config',{}).get('Repos',{}).items():
                self.title = title
                self.location = location
                break ## just get first instance.

        self.app.data['information'] =  {
            'title' : self.title.title(),
            'repo_name' : self.title,
            'location' : self.location
        }

        self.app.action = self.name + self.title
        frame = kwg.get('frame', None)
        row = 100
        if frame != None and self.location != None:
            self.index_headers(frame)
            for repo in self.get_repos(self.location):
                if self.app.action == self.name + self.title:
                    self.render_repository_row(frame, repo, row)
                    row += 1
                    frame.update()
                    self.app.content.config(scrollregion=self.app.content.bbox("all"))
                else:
                    break;

    def action_load_index(self, title, location):
        self.title = title
        self.location = location
        self.app.render_plugin(self)



    def register_menus(self, menubar):
        repo_menu = tk.Menu(menubar , tearoff=0)
        menubar.add_cascade(label='Repositories', menu=repo_menu)
        for title, location in self.app.data.get('config',{}).get('Repos',{}).items():
            repo_menu.add_command(label=title.title(), command=lambda title=title, location=location: self.action_load_index(title, location))

    def get_repos(self,path):
        """Generator that pulls the repo in a specific repo_type or folder, defined in section Repos in ~/wp_vars"""
        section_name = 'repo_%s'%self.title.lower()
        excludes = self.app.data.get('config',{}).get(section_name,{}).get('exclude', [])

        for subdir, dirs, files in os.walk(path):
            for dir in dirs:
                if (dir == '.git'):
                    ## Checks to see if there is an exclude in the ~/wp_vars, ie gravityforms
                    repo_name = os.path.basename(os.path.normpath(subdir))
                    if repo_name not in excludes:
                        os.chdir(subdir)
                        yield Repo(subdir)


    def add_repo_label(self, *arg, **kwg):
        frame = kwg.get('frame', None)
        label = None
        if frame != None:
            label = tk.Label(frame, text=kwg.get('repo_name', '??'),  )
        return label

    def index_headers(self, frame, row=10):
        ttk.Label(frame, text="Commits", background="#ccc", font="Helvetica 14 bold").grid(column=3,columnspan=3, row=row-1, sticky="ew")
        row_header = [
        ttk.Label(frame, text='Name'),
        ttk.Label(frame, text='Active Branch'),
        ttk.Label(frame, text="Status"),
        ttk.Label(frame, text="Active"),
        ttk.Label(frame, text="Dev"),
        ttk.Label(frame, text="Mast"),
        ttk.Label(frame, text="Latest\nTag\nBranch"),
        ttk.Label(frame, text="Latest\nTag\nMaster"),
        #ttk.Label(tab, text="Errors"),
        ttk.Label(frame, text='Branch\nHash'),
        ttk.Label(frame, text="Master\nHash")
        ]

        count = 0
        for data in row_header:
            data.config(background="#ddd")
            data.grid(column=count, row=row, padx=8, pady=8, sticky="W")
            count += 1


    def render_repository_row(self, frame, repo, row):
        padx = 8
        pady = 8

        status_color, data, commits = self.get_repo_health(self.title, repo)
        repo_name = os.path.basename(os.path.normpath(repo.working_dir))
        call = lambda defaultname=repo: self.action_repo_info(defaultname)


        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(column=0, columnspan=11, row=row, sticky='new')
        status_canvas = tk.Canvas(frame, width=32, height=32, bg=self.app.background, highlightthickness=0)
        status_canvas.create_oval(5,5,30,30, fill=status_color)

        row_data = [
            self.app.do_action('summary_repo_name', frame=frame, repo_name=repo_name, repo=repo, default=self.add_repo_label),
            ttk.Label(frame, text=repo.active_branch.name),
            status_canvas,
            ttk.Label(frame, text=len(commits.get('branch'))),
            ttk.Label(frame, text=len(commits.get('origin/development'))),
            ttk.Label(frame, text=len(commits.get('origin/master'))),
            ttk.Label(frame, text=data['branch'].get('tag','')),
            ttk.Label(frame, text=data['master'].get('tag','')),
            ttk.Label(frame, text=data['branch'].get('hash','')),
            ttk.Label(frame, text=data['master'].get('hash','')),
        ]
        count = 0;
        for data in row_data:
            data.grid(column=count, row=row, padx=padx, pady=pady, sticky="WS")
            count += 1


def setup(app):
    summary = Summary(app)
    app.register_class('Summary.instance', summary)
    app.register_menu('Summary.menu', summary.register_menus)
