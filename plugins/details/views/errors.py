from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext as tkst

def render_repository_errors(self, frame):
    """
    Shows debug code, and dirty files.
    """
    repo = self.repo
    content_text = tkst.ScrolledText(master=frame, wrap=WORD, height=8, width=100 )
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
    content_text.pack(fill=BOTH, expand=True, anchor="w")
