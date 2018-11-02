
from DevPlugin import DevopsAppPlugin
from git import Repo
import git
import os, sys

class Push(DevopsAppPlugin):
    commit_message = None
    commit_message_component = None
    synctoserver = None
    commit_version = None
    parent_instance = None
    repo = None

    def __init__(self, app):
        super().__init__(app)
        self.name = 'push'


    def check_push(self, remote):
        ''' checks to see if push is possible, if not it will fail process '''

        try:
            self.log(self.repo.git.push('--dry-run', 'origin', 'HEAD:%s'%remote), level='debug')
        except git.GitCommandError as gce:
            self.log('Might require merge from origin %s'%remote, level='error')
            return False
        return True

    def update_master(self):
        ''' Updates master, if tags are added, will eventually be removed '''

        self.repo.git.checkout('master')
        self.repo.git.pull()
        self.log(self.cmd(['git', 'merge', 'development']),level="debug")
        self.repo.git.push()
        self.repo.git.push('--tags')
        self.repo.git.pull()


    def add_tags(self):
        ''' This adds tags to branch '''

        if self.get_data('current_repo.version') != self.get_data('current_repo.latest_tag'):
            self.log(self.cmd(['git', 'tag', '-a', self.get_data('current_repo.version'), '-m', self.commit_message]))
            self.repo.git.push('--follow-tags')
            return True

    def action_update_local_branches(self, remote):
        ''' Updates all the local branches of master, development and release where applicable '''
        #TODO: eventurally remove update_master once the pipeline is successful.

        self.log('Commit was pushed to remote.', level="success")
        branch = self.repo.active_branch.name
        tags = False
        self.repo.git.checkout(remote)
        self.repo.git.pull()
        if self.commit_version.get():
            tags = self.add_tags()

        if remote != 'master' and tags:
            self.update_master()
            ## on master branch, and merging development, hopefully remote would be development at this point.
        try:
            self.repo.git.checkout('release')
            self.repo.git.pull()
        except git.GitCommandError as e:
            pass
        self.repo.git.checkout(branch)


    def action_commit_message(self, remote):
        '''
        This does the git add and git comit and tries to push to remote
        '''

        self.repo.git.add('.')
        self.repo.index.commit(self.commit_message)
        try:
            self.repo.git.push('origin', 'HEAD:%s'%remote)
            self.action_update_local_branches(remote)
        except git.GitCommandError as exc:
            self.log('SLOW DOWN PARTNER, you are trying to do something I can\'t do.  Go to the Git command line, and try to fix this mess. :)', level="error")
            self.log('An error occured while pushing to HEAD:%s from %s branch' % (remote, self.repo.active_branch.name), level='error')
            self.log(str(exc), level='error')
            return False
        return True

    def resolve_push_conflict(self, remote):
        self.log('should ask for commit only if dirty, and pull repo to merge.',level='debug')
        '''
        try:
            self.repo.git.pull()
            log('Pulled latest commits from origin/development', 'success')
        except git.GitCommandError as exc:
            log('An error occured while merging developemnt into %s' % self.repo.active_branch.name,'error')
            log(str(exc),'error')
            self.controller.notify_user('Fix Merge Updates.!', 'A merge was just performed, please view changed files, and fix conflicts.')
            return False
        '''

    def action_push(self):
        ''' This is called on clicking push button, triggers the process to push to remote. '''
        #TODO: the release will not update after and do_action push_successful, unless this is included into what ever hooks into this behavour.
        #TODO: Add synctoserver logic plugin.
        #TODO: update current version in self.app.data['current_repo'] when tags are added.
        #TODO: add resolve_push_conflict logic
        #TODO: Should have a test to see if push was successful

        ci_cd = self.get_data('current_repo.ci_cd', True)
        self.repo = self.get_repo()
        self.commit_message = self.commit_message_component.get(1.0,'end')
        remote = 'master'
        results = False
        if ci_cd:
            remote = 'development'
        if self.commit_message != None and len(self.commit_message.strip()) > 4 and self.check_push(remote):
            results = self.action_commit_message(remote)
        else:
            self.resolve_push_conflict(remote)

        if self.synctoserver.get():
            self.app.do_action('sync_to_server', repo=self.repo)

        if results:
            self.app.do_action('push_successful', ci_cd=ci_cd, repo=self.repo)
            #refreshes page.
            try:
                self.app.render_plugin(self.parent_instance)
            except:
                pass
        else:
            self.app.do_action('push_error', ci_cd=ci_cd, repo=self.repo)



    def render_commit_message(self, *arg, **kwg):
        ''' This is called from a do_action which is from the details plugin '''

        frame = kwg.get('frame', None)
        self.parent_instance = kwg.get('instance', {})
        if frame != None:
            self.render_repository_actions(frame)

    from .views.pushdialog import render_repository_actions
