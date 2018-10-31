from tkinter import ttk


def render_branches(self, frame):
    """
    Renders the branches, and options for the branches.
    """
    repo = self.repo
    row = 1;
    ttk.Label(frame, text="Branch", style="Bold.TLabel").grid(column=0, row=0, padx=4, pady=4, sticky="w")
    ttk.Label(frame, text="Count", style="Bold.TLabel").grid(column=1, row=0, padx=4, pady=4, sticky="w")
    ttk.Label(frame, text="Tag", style="Bold.TLabel").grid(column=2, row=0, padx=4, pady=4, sticky="w")
    ttk.Label(frame, text="Hash", style="Bold.TLabel").grid(column=3, row=0, padx=4, pady=4, sticky="w")
    ttk.Label(frame, text="Activate", style="Bold.TLabel").grid(column=4, row=0, padx=4, pady=4, sticky="w")
    ttk.Label(frame, text="Delete", style="Bold.TLabel").grid(column=5, row=0, padx=4, pady=4, sticky="w")
    ttk.Label(frame, text="Merge", style="Bold.TLabel").grid(column=6, row=0, padx=4, pady=4, sticky="w")

    branches_data = self.get_branch_stats(self.repo)
    for key, branch_data in branches_data.items():
        b_name, b_tag, b_count, b_diff, b_hash = branch_data
        count_text = b_count
        if len(b_diff) > 0:
            count_text = '%s (%s)'%(b_count,b_diff)

        label = ttk.Label(frame, text=b_name)
        count = ttk.Label(frame, text=count_text)
        tag = ttk.Label(frame, text=b_tag)
        hash = ttk.Label(frame, text=b_hash)

        ci_cd2 = False

        ci_cd = ((b_name == 'master' or b_name == 'development' or b_name == 'release')  and ci_cd2)
        active_branch = b_name == repo.active_branch.name
        is_dirty = (repo.is_dirty() or len(repo.index.diff(None)) > 0)

        if ci_cd or active_branch or is_dirty:
            abutton = ttk.Label(frame, text="")
            dbutton = ttk.Label(frame, text="")
            if len(b_diff) > 0 and b_name != 'master' and active_branch:
                mbutton = ttk.Button(frame, text="Merge", command=lambda arg1=repo, arg2=b_name: self.action_merge_branch(arg1, arg2))
                if (is_dirty):
                    mbutton.config(state=tk.DISABLED)
                mbutton.grid(column=6, row=row, padx=4, pady=4, sticky="w")

        else:
            abutton =  ttk.Button(frame, text="Activate", command=lambda arg1=repo, arg2=b_name: self.action_switch_branch(arg1, arg2))
            dbutton = ttk.Button(frame, text="Delete", command=lambda arg1=repo, arg2=b_name: self.action_delete_branch(arg1, arg2))

        if self.check_commit_error_status(branches_data, branch_data):
            label.config(style="Warn.TLabel")
            count.config(style="Warn.TLabel")
            tag.config(style="Warn.TLabel")
            hash.config(style="Warn.TLabel")

        if (b_name == repo.active_branch.name):

            label.config(style="Bold.TLabel")
            count.config(style="Bold.TLabel")
            tag.config(style="Bold.TLabel")
            hash.config(style="Bold.TLabel")

        label.grid(column=0, row=row, padx=4, pady=4, sticky="w")
        count.grid(column=1, row=row, padx=4, pady=4, sticky="w")
        tag.grid(column=2, row=row, padx=4, pady=4, sticky="w")
        hash.grid(column=3, row=row, padx=4, pady=4, sticky="w")
        abutton.grid(column=4, row=row, padx=4, pady=4, sticky="w")
        dbutton.grid(column=5, row=row, padx=4, pady=4, sticky="w")

        row += 1

    if ( not (repo.is_dirty() or len(repo.index.diff(None)) > 0)):
        self.app.do_action('details_pull_action', frame=frame, repo=repo, row=row)
