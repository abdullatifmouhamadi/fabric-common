from settings import APPS, APP_STAGES
from fabric_common.common.deploy import Deployable



class Prestashop(Deployable):

    def __init__(self, app_name, stage_name, params):
        Deployable.__init__(self, 
                            stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)
        
    def update_nginx_template(self):
        MYPORT = '80' #self.port
        MYHOST = self.stage['host']
        NGINX_FILENAME = self.nginx_filename
        WORKINGDIR = self.appDir + '/src/prestashop/'

        self.rc.sed(self.nginx_available, 'MYPORT', MYPORT)
        self.rc.sed(self.nginx_available, 'MYHOST', MYHOST)
        self.rc.sed(self.nginx_available, 'NGINX_FILENAME', NGINX_FILENAME)
        self.rc.sed(self.nginx_available, 'WORKINGDIR', WORKINGDIR.replace('/', r'\/'))

        # link
        self.rc.linksoft(self.nginx_available, self.nginx_enabled)

        # reload nginx
        self.rc.reloadnginx()

    def config_nginx_template(self):
        print("\n\n==> config_nginx_template\n\n")
        self.rc.copy(src    = self.appDir + '/deploy/archlinux/template-nginx',
                     target = self.nginx_available)

        self.update_nginx_template()



    def install_prestashop(self):
        SCRIPT_PATH = self.appDir + '/script/'
        APP_PATH    = self.appDir + '/src/prestashop/'
        self.rc.run("cd {} && python setup.py".format(SCRIPT_PATH))
        self.rc.sudo("chmod -R 755 {}".format(APP_PATH))



    def deploy(self):
        self.pre_deploy()

        # setup
        self.setup_git_env()


        #
        self.install_prestashop()


        # nginx
        self.config_nginx_template()



        self.post_deploy()