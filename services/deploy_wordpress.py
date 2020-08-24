from settings import APPS, APP_STAGES
from fabric_common.common.deploy import Deployable



class Wordpress(Deployable):

    def __init__(self, app_name, stage_name, params):
        Deployable.__init__(self, 
                            stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)




    def deploy(self):
        self.pre_deploy()




        #cerbot - carefull- can make crash nginx
        self.setup_certbot_ssl()

        if self.rc.file_exists(pattern = self.certbot_fullchain):
            self.enable_nginx_ssl()
        
        self.post_deploy()