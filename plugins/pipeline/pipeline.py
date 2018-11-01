from DevPlugin import DevopsAppPlugin
import requests, urllib
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
        if self.remote_status(''):
            pass

    def push_successful(self, *a, **kwg):
        repo = kwg.get('repo')
        ci_cd = kwg.get('ci_cd')
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
            urllib.request.urlopen(url)
            online = True
        except urllib.error.URLError as error:
            pass
        except urllib.error.HTTPError as error:
            pass

        return online
