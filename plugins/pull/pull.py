from DevPlugin import DevopsAppPlugin
from tkinter import ttk
import os

class Pull(DevopsAppPlugin):
    '''
    Class Pull
    ~~~~~~~~~~

    Creates a GUI and a terminal program to pull feature branch, and clone repos.
    * A symlink should be created ie ln -s ./plugins/pull/__init__.py /usr/local/bin/wpull
    * Usage
        * gui button [Add Repo] (top of all summary pages.)
        * gui button [Pull] (below branches on details page)
        * terminal - pulls feature branch   [Command] wpull
        * terminal - adds clone repo        [Command] wpull -c,--clone {clone url}
        * terminal - shows these docs.      [Command] wpull -d, --docs
    '''
    #TODO: What are we going to do with wpull for non cd_ci.
    repo = None
    parent_instance = None

    def __init__(self, app):
        ''' initializes super, and sets name to pull '''
        super().__init__(app)
        self.name = 'pull'

    def term_pull(self, data):
        ''' Terminal [Pull feature branch] - allows wpull to be executed. where ln -s .plugins/pull/__init__.py /usr/local/bin/wpull '''

        self.term_show_title('BCGov Pull')
        dirname = os.path.abspath('.')
        if self.term_question('Is this the repo to pull from: %s [(Y)es/(N)o] (y) '%dirname, 'y', case_sensitive=True) == 'y':
            ci_cd = self.term_question('Is there a development branch for ci_cd [(Y)es/(N)o] (y) ', 'y', case_sensitive=True) == 'y'
            bname = self.term_question("Give Jira Ticket number or branch name?  ")
            self.do_pull(bname, ci_cd)
            self.log(self.cmd(['git', 'branch', '-vv']))



    def term_clone(self, data, clone_url):
        ''' Terminal [Clone Repo] - allows wpull -c {clone url} to be executed. where ln -s .plugins/pull/__init__.py /usr/local/bin/wpull '''
        #TODO: if incorrect path, then maybe give input option for correct path.
        #TODO: if incorrect clone url, then keep asking until correct clone url.
        #TODO: Show indication that this has been done.

        self.term_show_title('BCGov Clone')
        dirname = os.path.abspath('.')
        if self.term_question('Is this the parent directory you want to clone new repo: %s? [(Y)es/(N)o] (y) '%dirname, 'y', case_sensitive=True) == 'y':
            if clone_url == None:
                clone_url = self.term_question('Please Enter the repo clone url. ')
            if self.term_question('Is this the clone url: %s? [(Y)es/(N)o] (y) '%clone_url, 'y', case_sensitive=True) == 'y':
                self.clone(clone_url, dirname)
            else:
                self.log('Re-run the program with the correct clone url.')
        else:
            self.log('Please switch to the current directory and re-run program.')

    def create_development_branch(self):
        ''' Creates Development Branch   '''
        #TODO: -- might want to delete it locally after creating, shouldn't need it anymore
        #TODO: convert to using gitpython

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
        #TODO: convert to using gitpython

        fetch = self.cmd(['git', 'show-ref', 'refs/heads/%s'%name])
        if fetch == None:
            origin_name = 'master'
            if development:
                origin_name = 'development'
            self.log('Looks like %s branch has not been created, Creating branch..' %name)
            self.cmd(['git', 'branch', '--track', name, 'origin/%s'%origin_name])
            self.cmd(['git', 'checkout', name])
            return True

    def do_pull(self, branch_name, ci_cd):
        ''' Convergent point for both the gui and terminal for pull of feature branch '''

        branch_name = 'feature_%s'%branch_name
        if ci_cd:
            self.create_development_branch()
        results = self.create_feature_branch(branch_name, ci_cd)
        if results:
            self.log('Feature branch feature_%s was created and checked out' %branch_name, level='success')
        else:
            self.log('Feature branch feature_%s was not created' %branch_name, level='error')


    def action_pull(self):
        ''' GUI - action to pull another version.'''

        self.repo  = self.get_repo()
        ci_cd = self.get_data('current_repo.ci_cd', True)
        branch_name = self.askinput_modal("Feature Branch Name", 'Please Enter feature branch name')
        if branch_name != None and len(branch_name) > 2:
            self.do_pull(branch_name, ci_cd)
            try:
                self.app.render_plugin(self.parent_instance)
            except:
                pass

    def get_button(self, *arg, **kwgs):
        '''
        GUI - This adds the pull button below the branches to create feature branch
        do_action - details_pull_action
        '''

        frame = kwgs.get('frame', None)
        row = kwgs.get('row', 100)
        self.parent_instance = kwgs.get('instance')
        if frame != None and self.parent_instance != None:
            ttk.Button(frame, text="Pull", command=lambda: self.action_pull()).grid(column=0, row=row, padx=4, pady=4, sticky="w")

    def clone(self, clone_name, repo_type_dir):
        ''' This is the convergent point for terminal and gui for cloning a repo '''

        if clone_name != None and len(clone_name) > 2:
            filename_w_ext = os.path.basename(clone_name)
            git_dir, file_extension = os.path.splitext(filename_w_ext)
            os.chdir(repo_type_dir)
            self.cmd(['git','clone', clone_name])
            os.chdir('%s/%s'%(repo_type_dir,git_dir))
            self.log(os.getcwd())
            return True

    def action_add_repo(self):
        ''' GUI this is the action from hitting the Add Repo button '''

        repo_type_dir = self.get_data('information.location')
        clone_name = self.askinput_modal("Repo Remote url", 'Please Enter the repo clone url')
        if self.clone(clone_name, repo_type_dir):
            try:
                self.app.render_plugin(self.parent_instance)
            except:
                pass

    def get_clone_button(self, *arg, **kwgs):
        '''
        GUI - this is how the Add Repo button gets created
        do_action - page_header_after
        '''

        frame = kwgs.get('frame')
        column = kwgs.get('column')
        self.parent_instance = kwgs.get('instance')
        if frame != None and self.parent_instance.name == 'summary':
            ttk.Button(frame, text="Add Repo", command=lambda: self.action_add_repo()).grid(column=column, row=1, padx=4,pady=4, sticky="e")
