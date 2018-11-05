from DevPlugin import DevopsAppPlugin
import requests, urllib, os, sys
from requests.auth import HTTPBasicAuth

class Pipeline(DevopsAppPlugin):
    repo = None
    ci_cd = True

    def __init__(self, app):
        super().__init__(app)
        self.name = 'pipeline'
        self.config = self.get_data('config.plugin_pipeline')

    def sync_to_server(self, *a, **kwg):
        ''' '''
        #TODO: add a do_action to add sync to server from pipeline.
        repo = kwg.get('repo')
        type = self.app.get_data('information.repo_type')
        test_url = self.app.get_data('config.repo_%s.rsync_test_url'%type, False)

        if test_url and self.remote_status(test_url):
            data = {
                'type' : type,
                'rsync_remote' : self.app.get_data('config.repo_%s.rsync_remote'%type),
                'user' : self.app.get_data('config.User.user_name'),
                'local_path' : repo.working_dir
            }
            servers = self.app.get_data('config.repo_%s.rsync_servers'%type)
            if isinstance(servers, list):
                for server in servers:
                    self.rsync(server, data)
            elif isinstance(servers, str):
                self.rsync(servers, data)


    def rsync(self, server, data):
        """ Does rsync to servers """
        dest = "%s@%s:%s%s/" % (data.get('user'), server, data.get('rsync_remote'), os.path.split(data.get('local_path',''))[-1])
        rsync_list = [
            'rsync',
            '-a',
            data.get('local_path','')+'/',
            dest,
            "--omit-dir-times",
            "--no-perms",
            "--no-owner",
            "--no-group",
            "--chmod=g+rwX",
            "--delete",
            "--itemize-changes",
            "--exclude=node_modules",
            "--exclude=.cache-loader",
            "--exclude=bower_components",
            "--exclude=.git"

        ]
        if data.get('debug',False):
            rsync_list.append("--verbose")
            rsync_list.append("--dry-run")


        cmd = self.cmd(rsync_list)
        self.log(cmd,level='debug')
        if cmd != None:
            self.log('Synced %s to %s'%(data.get('local_path'), dest),level='success')


    def push_successful(self, *a, **kwg):
        repo = kwg.get('repo')
        ci_cd = kwg.get('ci_cd')

        if ci_cd:
            self.trigger_jenkins()


    def push_error(self, *a, **kwg):
        repo = kwg.get('repo')
        ci_cd = kwg.get('ci_cd')


    def trigger_jenkins(self):
        url = self.config.get('url','')
        test_url = self.config.get('test_url', url)
        if self.remote_status(test_url):
            payload = {
                'token' : self.config.get('token',''),
                'type'  : self.get_data('information.repo_type'),
                'repo'  : self.get_data('current_repo.repo_name')
            }
            self.log('Triggering Jenkins Pipeline %s'%url)
            self.log(url, payload, level='debug')
            try:
                r = requests.post(url, data=payload,  auth=HTTPBasicAuth(self.config.get('user',''), self.config.get('password','')))
                if r.status_code  in [200, 201]:
                    self.log('Jenkins pipline has been successfully started', level='success')
                else:
                    self.log('Jenkins pipeline has failed, see debug log for more details', level='error')
                    self.log(r.status_code, level='debug')
                    self.log(r.header, level='debug')
                self.log(payload, level='debug')
            except requests.exceptions.HTTPError as err:
                self.log('HTTPError Connection error with Jenkins server',level='error')
                self.log(str(err),level='error')
            except requests.exceptions.ConnectionError as err:
                self.log('Connection Error with Jenkins server', level='error')
                self.log(str(err),'error')
        else:
            self.log('Jenkins server does not appear to be online', level='error')

    def remote_status(self, url):
        online = False
        try:
            urllib.request.urlopen(url,timeout=1)
            online = True
        except urllib.error.URLError as error:
            pass
        except urllib.error.HTTPError as error:
            pass

        return online
