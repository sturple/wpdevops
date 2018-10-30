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
            button = tk.Button(frame, text=kwg.get('repo_name', '??'), command=call  )
        return button

    def render_repository(self, frame):
        '''
        This creates the frames for the repository Information
        '''


        self.set_page_header(frame)
        #information
        info_frame = tk.LabelFrame(frame, text="Information")
        info_frame.config(relief=tk.RIDGE)
        self.render_repository_info(info_frame)

        branch_frame = tk.LabelFrame(frame, text="Braches")
        branch_frame.config(relief=tk.SUNKEN)
        self.render_branches(branch_frame)

        #action frame
        action_frame = tk.LabelFrame(frame, text="Actions")
        self.app.do_action('details_push_commit', frame=action_frame)
        #self.render_repository_actions(action_frame)

        info_frame.grid(row=10, column=0, padx=8, pady=8, sticky="nw")
        branch_frame.grid(row=10, column=1, padx=8, pady=8, sticky="nw")
        action_frame.grid(row=11, column=0, padx=8, pady=8, sticky="nw")

    def render_repository_info(self, frame):
        """
        This frame has information about the repositoryself.
        Includes the message dialog that has debug code and dirty files.
        """
        repo = self.repo
        repo_name = os.path.basename(os.path.normpath(repo.working_dir))

        version_frame = tk.Frame(frame)
        ttk.Label(version_frame, text=self.get_data('current_repo.version')).pack(anchor="w",side=tk.LEFT)
        ttk.Button(version_frame, text="Change Version", command=lambda: self.action_change_version()).pack(anchor="w", side=tk.RIGHT)

        status_color, _, _ = self.get_repo_health(repo_name, repo)
        status_canvas = tk.Canvas(frame, width=32, height=32, bg=self.app.background, highlightthickness=0)
        status_canvas.create_oval(2,2,25,25, fill=status_color)

        components = [
            (ttk.Label(frame, text="Name"), tk.Label(frame, text=repo_name)),
            (ttk.Label(frame, text="Active Branch"), tk.Label(frame, text=repo.active_branch.name)),
            (ttk.Label(frame, text="Version File"), tk.Label(frame, text=self.get_data('current_repo.version_file'))),
            (ttk.Label(frame, text="Version"), version_frame),
            (ttk.Label(frame, text="Latest Tag"), tk.Label(frame, text=self.get_data('current_repo.latest_tag'))),
            (ttk.Label(frame, text="Health"), status_canvas),

        ]
        row = 100;
        for label, value in components:
            label.config(font="Helvetica 14 bold")
            label.grid(column=0, row=row, padx=4, pady=4, sticky="W")
            value.grid(column=1, row=row, padx=4, pady=4, sticky="W")
            row += 1

        #error frames
        error_frame = tk.LabelFrame(frame, text="")
        self.render_repository_errors(error_frame)
        error_frame.grid(row=row, column=0,  columnspan=2, padx=8, pady=8, sticky="w")

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


    def render_branches(self, frame):
        """
        Renders the branches, and options for the branches.
        """
        repo = self.repo
        row = 1;
        ttk.Label(frame, text="Branch", font="Helvetica 14 bold").grid(column=0, row=0, padx=4, pady=4, sticky="w")
        ttk.Label(frame, text="Count", font="Helvetica 14 bold").grid(column=1, row=0, padx=4, pady=4, sticky="w")
        ttk.Label(frame, text="Tag", font="Helvetica 14 bold").grid(column=2, row=0, padx=4, pady=4, sticky="w")
        ttk.Label(frame, text="Hash", font="Helvetica 14 bold").grid(column=3, row=0, padx=4, pady=4, sticky="w")
        ttk.Label(frame, text="Activate", font="Helvetica 14 bold").grid(column=4, row=0, padx=4, pady=4, sticky="w")
        ttk.Label(frame, text="Delete", font="Helvetica 14 bold").grid(column=5, row=0, padx=4, pady=4, sticky="w")
        ttk.Label(frame, text="Merge", font="Helvetica 14 bold").grid(column=6, row=0, padx=4, pady=4, sticky="w")

        branches_data = self.get_branch_stats(self.repo)
        for key, branch_data in branches_data.items():
            b_name, b_tag, b_count, b_diff, b_hash = branch_data
            count_text = b_count
            if len(b_diff) > 0:
                count_text = '%s (%s)'%(b_count,b_diff)

            label = tk.Label(frame, text=b_name, bg=self.app.background)
            count = tk.Label(frame, text=count_text, bg=self.app.background)
            tag = tk.Label(frame, text=b_tag, bg=self.app.background)
            hash = tk.Label(frame, text=b_hash, bg=self.app.background)

            ci_cd2 = False

            ci_cd = ((b_name == 'master' or b_name == 'development' or b_name == 'release')  and ci_cd2)
            active_branch = b_name == repo.active_branch.name
            is_dirty = (repo.is_dirty() or len(repo.index.diff(None)) > 0)

            if ci_cd or active_branch or is_dirty:
                abutton = tk.Label(frame, text="", bg=self.app.background)
                dbutton = tk.Label(frame, text="", bg=self.app.background)
                if len(b_diff) > 0 and b_name != 'master' and active_branch:
                    mbutton = tk.Button(frame, text="Merge", command=lambda arg1=repo, arg2=b_name: self.action_merge_branch(arg1, arg2))
                    if (is_dirty):
                        mbutton.config(state=tk.DISABLED)
                    mbutton.grid(column=6, row=row, padx=4, pady=4, sticky="w")

            else:
                abutton =  ttk.Button(frame, text="Activate", command=lambda arg1=repo, arg2=b_name: self.action_switch_branch(arg1, arg2))
                dbutton = ttk.Button(frame, text="Delete", command=lambda arg1=repo, arg2=b_name: self.action_delete_branch(arg1, arg2))

            if self.check_commit_error_status(branches_data, branch_data):
                label.config(fg="red")
                count.config(fg="red")
                tag.config(fg="red")
                hash.config(fg="red")

            if (b_name == repo.active_branch.name):
                font="Helvetica 14 bold"
                label.config(font=font)
                count.config(font=font)
                tag.config(font=font)
                hash.config(font=font)

            label.grid(column=0, row=row, padx=4, pady=4, sticky="w")
            count.grid(column=1, row=row, padx=4, pady=4, sticky="w")
            tag.grid(column=2, row=row, padx=4, pady=4, sticky="w")
            hash.grid(column=3, row=row, padx=4, pady=4, sticky="w")
            abutton.grid(column=4, row=row, padx=4, pady=4, sticky="w")
            dbutton.grid(column=5, row=row, padx=4, pady=4, sticky="w")

            row += 1

        if ( not (repo.is_dirty() or len(repo.index.diff(None)) > 0)):
            self.app.do_action('details_pull_action', frame=frame, repo=repo, row=row)


def setup(app):
    details = Details(app)
    app.register_class('Details.instance', details)
    app.add_action('summary_repo_name', details.add_repo_button)
