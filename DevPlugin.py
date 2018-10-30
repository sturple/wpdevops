import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import simpledialog, filedialog
from tkinter import scrolledtext as tkst
from git import Repo
import git
import os, sys, re, subprocess

class DevopsAppPlugin(object):
    def __init__(self, app):
        self.app = app
        self.startup  = False

    def log(self, *a, **kwg):
        self.app.log(*a, **kwg)

    def get_data(self, namespace="", default=None):
        """This uses namespace to parse through config file ie config.Repos.plugins """
        spaces = re.sub(r'\s', '', namespace).split('.');
        v = self.app.data
        for space in spaces:
            try:
                v = v.get(space,default)
            except AttributeError as e:
                pass
        return v

    def set_page_header(self, frame):
        ''''
        repo = self.controller.model.repo
        data = self.controller.model.repo_config
        title = tk.Label(frame, text=data.get('title', ''), font="Helvetica 22 bold", bg=self.background)
        path = tk.Label(frame, text=data.get('root_path',''), bg=self.background)
        title.grid(column=0, row=1, padx=4, pady=4, sticky="w")
        path.grid(column=0, row=2, padx=4, pady=4, sticky="w")
        if repo != None:
            breadcrumb = tk.Frame(frame)
            tk.Button(breadcrumb, text="Repository", command=lambda: self.controller.action_load_index(data['repo_type'])).pack(anchor="w", side=tk.LEFT)
            tk.Button(breadcrumb, text="Refresh", command=lambda: self.controller.action_repo_info(repo)).pack(anchor="w", side=tk.LEFT)
            breadcrumb.grid(column=0, row=3, padx=4, pady=4, columnspan=2, sticky="w")
        '''


    def get_repo_health(self, type, repo):
        """Used both on the index, and info page.  Used to determine health, and the Red/Orange/Green dot"""
        PASS="green"
        WARN="orange"
        FAIL="red"
        status_color=PASS
        data = {}
        errors = []
        repo_name = os.path.basename(os.path.normpath(repo.working_dir))
        ci_cd_flag = self.get_data('config.repo_%s.ci_cd.abc'%type, False)


        repo_name = os.path.basename(os.path.normpath(repo.working_dir))
        if str(repo.active_branch.name) == 'master' and ci_cd_flag:
            errors.append(('Active branch should not be master', 'warn'))
            status_color=WARN

        if str(repo.active_branch.name) == 'development' and ci_cd_flag:
            errors.append(('Active branch should not be development', 'warn'))
            status_color=WARN

        if str(repo.active_branch.name) == 'release' and ci_cd_flag:
            errors.append(('Active branch should not be release', 'warn'))
            status_color=WARN

        for branch in ['origin/development']:
            if len(self.check_branch(repo, branch)) > 0 and ci_cd_flag:
                status_color=WARN
                errors.append(('No Development branch.', 'warn'))

        for branch in ['origin/master']:
            if len(self.check_branch(repo, branch)) > 0:
                status_color=WARN
                errors.append(('No origin/master branch.', 'warn'))
                errors.append(('This could be due to error in repo, or 3rd party plugin', 'debug'))

        btag = ''
        mtag = ''
        try:
            btag = repo.git.describe('--abbrev=0', '--tags')
            mtag = repo.git.describe('origin/master', '--abbrev=0', '--tags')
        except git.GitCommandError as exc:
            #self.log('Git tag error, probably because no tags are available', level='debug')
            #self.log(exc, level='debug')
            pass

        try:
            data = {'branch' : {}, 'master' : {}}
            data['branch'] = {
                'hash' : repo.git.log('-n','1','--pretty=format:%H', repo.active_branch.name)[0:7],
                'tag'  : btag
            }

            data['master'] = {
                'hash' : repo.git.log('-n','1','--pretty=format:%H', 'origin/master')[0:7],
                'tag'  : mtag
            }

            if data['branch'].get('hash', '') != data['master'].get('hash', ''):
                status_color=WARN
                errors.append(("Branch hash is not the same as origin/master hash", 'warn'))
        except git.GitCommandError as exc:
            status_color=FAIL
            errors.append(('Issue finding origin/master', 'error'))
            self.log(exc, level='debug')

        staged_files = repo.git.status('--short', '-unormal')
        if repo.is_dirty() or len(repo.index.diff(None)) > 0 or len(staged_files) > 3:
            errors.append(('There are changes that need to be commited.', 'error'))
            status_color=FAIL

        commits = self.get_branch_commits(repo, repo.active_branch.name);

        if len(commits.get('branch')) < len(commits.get('origin/development')) and len(commits.get('origin/development')) > 0:
            status_color=FAIL
            errors.append(('Branch %s  is behind origin/development' %(repo.active_branch.name), 'error'))

        if len(errors) > 0:
            self.log('[Health Issues -- %s]'%(repo_name))
            for msg, type in errors:
                self.log(msg,level=type)
        return status_color, data, commits

    def get_branch_commits(self, repo, branch):
        """gets all the branch commits active, development, origin/development, master and origin/master"""
        branch = ''
        dev = ''
        org_dev = ''
        master = ''
        org_master = ''
        if len(self.check_branch(repo, repo.active_branch.name)) == 0:
            branch = list(repo.iter_commits(repo.active_branch.name))

        if len(self.check_branch(repo, 'development')) == 0:
            dev = list(repo.iter_commits('development'))

        if len(self.check_branch(repo, 'origin/development')) == 0:
            org_dev = list(repo.iter_commits('origin/development'))

        if len(self.check_branch(repo, 'master')) == 0:
            master = list(repo.iter_commits('master'))

        if len(self.check_branch(repo, 'origin/master')) == 0:
            org_master = list(repo.iter_commits('origin/master'))

        return{
            'branch' : branch,
            'development' : dev,
            'origin/development' : org_dev ,
            'master' : master,
            'origin/master' : org_master
        }

    def check_branch(self, repo, branch='master'):
        try:
            repo.git.rev_parse('--verify', branch)
            return ''
        except git.GitCommandError as exc:
            return 'No %s branch\n' % branch

    def get_branch_stats(self, repo):

        """ Gets branch stats used for info page.  This is used with check_commit_error_status to update notifications on info page."""

        type = 'plugins'
        ci_cd_flag = self.get_data('config.repo_%s.ci_cd.abc'%type, False)

        branches_data = {}
        for branch in self.repo.branches:
            commits=''
            b_tag = ''
            origin_commits = {}
            try:
                b_tag = repo.git.describe(branch.name, '--abbrev=0', '--tags')
            except git.GitCommandError as exc:
                pass

            branch_name = branch.name
            if (branch.name == 'master' or branch.name == 'development' or branch.name == 'release') and ci_cd_flag:
                branch_name = "origin/%s"%branch.name

            if len(self.check_branch(repo, branch_name)) == 0:
                    commits = list(repo.iter_commits(branch_name))
                    ahead_commits = {}
                    behind_commits = {}
                    diff_count =''
                    origin = 'master'
                    if ci_cd_flag:
                        origin = 'development'

                    try:
                        ahead_commits = list(repo.iter_commits('origin/%s..heads/%s'%(origin, branch_name)))
                        behind_commits = list(repo.iter_commits('heads/%s..origin/%s'%(branch_name,origin)))
                    except git.GitCommandError as exc:
                        pass

                    if len(ahead_commits) > 0:
                        diff_count = '+%d'%len(ahead_commits)
                    if len(behind_commits) > 0:
                        diff_count = '-%d'%len(behind_commits)
                    sha = repo.git.log('-n','1','--pretty=format:%H', branch_name)
                    hash_value = sha[0:7]
                    origin_commits[branch.name] = len(commits)

            branches_data[branch.name]=(branch.name,b_tag,len(commits),diff_count,hash_value)
        return branches_data

    def check_commit_error_status(self, branches_data, branch_data):
        """Logic to determine notifications on info page."""

        type = 'plugin'
        ci_cd_flag = self.get_data('config.repo_%s.ci_cd.abc'%type, False)

        b_name, b_tag, b_count, b_diff, b_hash = branch_data
        m_name, m_tag, m_count, m_diff, m_hash = branches_data.get('master', ('??master',None,0,0,0))
        d_name, d_tag, d_count, d_diff, d_hash = branches_data.get('development', ('??development',None,0,0,0))
        r_name, r_tag, r_count, r_diff, r_hash = branches_data.get('release', ('??release',None,0,0,0))
        error_flag = False
        if b_name == 'master' and ci_cd_flag:
            if b_count > d_count:
                log('Master branch is ahead of development branch', 'warn')
                error_flag = True
            pass
        elif b_name == 'development':
            pass
        elif b_name == 'release':
            if  b_count > d_count:
                log('Release branch is ahead of Development branch', 'warn')
                error_flag = True
        else:
            if b_count > d_count and ci_cd_flag:
                log('%s branch is ahead of development branch, development will need to be merged' % b_name,'warn')
                error_flag = True
            if b_count < d_count and ci_cd_flag:
                log('%s branch is behind development branch, development will need to be merged' % b_name,'warn')
                error_flag = True
        return error_flag


    def cmd(self, cmd, msg='Error %s'):
        """ this is a wrapper for subprocess.check_output"""
        output = ''
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            if isinstance(output, bytes):
                output = output.decode("utf-8")
        except subprocess.CalledProcessError as exc:
            output = exc.output;
            if isinstance(output, bytes):
                output = output.decode("utf-8")
            return None
        return output.strip('"').strip()


    def check_debug_code(self):
        return self.cmd([
            'egrep',
            '-rni',
            '--exclude-dir=./node_modules',
            '--exclude-dir=./bower_components',
            '--exclude-dir=./.git',
            '--exclude-dir=./vendor',
            '--exclude-dir=./dist',
            '--exclude-dir=./.cache-loader',
            '.*(error_log|var_dump|print_r|console\.(log|debug)).*',
            '.'
        ], 'Error %s')

    def get_version(self, path):
        """ Gets the version from css or php file"""
        for roots, dirs, fnames in os.walk(path):
            for fname in fnames:
                if fname.endswith('.php') or fname.endswith('.css'):
                    shpfiles = []
                    shpfiles.append(os.path.join(roots, fname))
                    fullpath = shpfiles[0]
                    v = self.cmd(['awk', '/Version/{printf $NF}', fullpath], 'AWK cmd error %s')
                    if (len(v)) > 0:
                        return 'v'+v, fullpath.replace(path,'')
        return '',''
