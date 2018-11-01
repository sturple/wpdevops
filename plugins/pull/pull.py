from DevPlugin import DevopsAppPlugin
from tkinter import ttk
import os

class Pull(DevopsAppPlugin):

    repo = None
    parent_instance = None

    def __init__(self, app):
        super().__init__(app)
        self.name = 'pull'


    def create_development_branch(self):
        ''' Creates Development Branch   '''
        #TODO: -- might want to delete it locally after creating, shouldn't need it anymore

        self.log('Create Branch(s)\nChecking for development', level='debug')
        fetch = self.cmd(['git','fetch','origin','development'])
        if fetch == None:
            self.log('Looks like development branch has not been created, Creating branch..', level='debug')
            self.log(self.cmd(['git', 'checkout', '-B', 'development']),'debug')
            self.log ('Pushing development branch to remote.', 'debug' )
            self.log(self.cmd(['git', 'push', '--set-upstream', 'origin', 'development']), level='debug')
            self.cmd(['git', 'fetch', '--all'])
            return True
        else:
            self.cmd(['git', 'fetch', '--all'])
            self.cmd(['git','checkout','development'])
            self.log(self.cmd(['git', 'pull']),level='debug')

    def create_feature_branch(self, name, development=True):
        ''' Create feature branch and track it to origin/development so can use simple push and pull no mergers '''

        fetch = self.cmd(['git', 'show-ref', 'refs/heads/%s'%name])
        if fetch == None:
            origin_name = 'master'
            if development:
                origin_name = 'development'
            self.log('Looks like %s branch has not been created, Creating branch..' % name)
            self.cmd(['git', 'branch', '--track', name, 'origin/%s'%origin_name])
            self.cmd(['git', 'checkout', name])
            return True


    def action_pull(self):
        ''' action to pull another version.'''
        self.repo  = self.get_repo()
        ci_cd = self.get_data('current_repo.ci_cd', True)

        branch_name = self.askinput_modal("Feature Branch Name", 'Please Enter feature branch name')
        if branch_name != None and len(branch_name) > 2:
            branch_name = 'feature_%s'%branch_name
            if ci_cd:
                self.create_development_branch()
            results = self.create_feature_branch(branch_name, ci_cd)
            if results:
                self.log('Feature branch feature_%s was created and checked out' %branch_name, level='success')
            else:
                self.log('Feature branch feature_%s was not created', level='error')
            try:
                self.app.render_plugin(self.parent_instance)
            except:
                pass

    def get_button(self, *arg, **kwgs):
        frame = kwgs.get('frame', None)
        row = kwgs.get('row', 100)
        self.parent_instance = kwgs.get('instance')
        if frame != None and self.parent_instance != None:
            ttk.Button(frame, text="Pull", command=lambda: self.action_pull()).grid(column=0, row=row, padx=4, pady=4, sticky="w")



    def action_add_repo(self):
        repo_type_dir = self.get_data('information.location')
        self.log('adding repo.. yah %s '%repo_type_dir)
        clone_name = self.askinput_modal("Repo Remote url", 'Please Enter the repo clone url')
        if clone_name != None and len(clone_name) > 2:
            filename_w_ext = os.path.basename(clone_name)
            git_dir, file_extension = os.path.splitext(filename_w_ext)
            os.chdir(repo_type_dir)
            self.cmd(['git','clone', clone_name])
            os.chdir('%s/%s'%(repo_type_dir,git_dir))
            self.log(os.getcwd())
            try:
                self.app.render_plugin(self.parent_instance)
            except:
                pass


    def get_clone_button(self, *arg, **kwgs):
        frame = kwgs.get('frame')
        column = kwgs.get('column')
        self.parent_instance = kwgs.get('instance')
        if frame != None and self.parent_instance.name == 'summary':
            ttk.Button(frame, text="Add Repo", command=lambda: self.action_add_repo()).grid(column=column, row=1, padx=4,pady=4, sticky="e")
