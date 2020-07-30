from settings import APPS, APP_STAGES
from fabric_common.common.deploy import Deployable

class Static(Deployable):

    def __init__(self, app_name, stage_name, params):
        Deployable.__init__(self, 
                            stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)  


    def update_nginx_template(self):
        print("==> config_nginx_template")
        MYHOST = self.stage['host']
        NGINX_FILENAME = self.nginx_filename
        WORKINGDIR = self.appDir + '/project/src/'

        # replace
        self.rc.sed(pattern = self.nginx_available,
                    old     = 'MYHOST',
                    new     = MYHOST)
        self.rc.sed(pattern = self.nginx_available,
                    old     = 'NGINX_FILENAME',
                    new     = NGINX_FILENAME)
        self.rc.sed(pattern = self.nginx_available,
                    old     = 'WORKINGDIR',
                    new     = WORKINGDIR.replace('/', r'\/'))
        
        # link
        self.rc.linksoft(src    = self.nginx_available,
                         target = self.nginx_enabled)

        # reload nginx
        self.rc.reloadnginx()

    def config_nginx_template(self):
        print("==> config_nginx_template")
        self.rc.copy(src    = self.appDir + '/deploy/archlinux/jycrois.com.website-stage',
                     target = self.nginx_available)

        self.update_nginx_template()


    def enable_nginx_ssl(self):
        print("==> enable_nginx_ssl")
        # enable them
        self.rc.copy(src    = self.appDir + '/deploy/archlinux/jycrois.com.website-stage-ssl',
                     target = self.nginx_available)

        self.update_nginx_template()



        
    def deploy(self):
        self.pre_deploy()

        # setup
        self.setup_git_env()

        # nginx
        self.config_nginx_template()


        #cerbot - carefull- can make crash nginx

        self.setup_certbot_ssl()

        if self.rc.file_exists(pattern = self.certbot_fullchain):
            self.enable_nginx_ssl()
            
    
        self.post_deploy()