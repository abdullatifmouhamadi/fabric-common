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

    def enable_nginx_ssl(self):
        print("\n\n==> enable_nginx_ssl\n\n")
        # enable them
        self.rc.copy(src    = self.appDir + '/deploy/archlinux/template-nginx-ssl',
                     target = self.nginx_available)

        self.update_nginx_template()

    def install_prestashop(self):
        SCRIPT_PATH = self.appDir + '/script/'
        APP_PATH    = self.appDir + '/src/prestashop/'
        self.rc.run("cd {} && python setup.py".format(SCRIPT_PATH))
        self.rc.sudo("chmod -R 755 {}".format(APP_PATH))

    def run_startup_script(self):
        print("\n\n==> running startup scripts\n\n")
        SCRIPT_PATH = self.appDir + '/script/'
        APP_PATH    = self.appDir + '/src/prestashop/'
        self.rc.copy(src    = self.appDir + '/script/startup.php',
                     target = APP_PATH + '/startup.php')


        #self.rc.run("cd {} && php72 --version".format(APP_PATH))
        self.rc.run("cd {} && php72 startup.php".format(APP_PATH))




    def deploy(self):
        self.pre_deploy()

        # setup
        self.setup_git_env()


        #
        self.install_prestashop()


        # nginx
        self.config_nginx_template()

        
        #cerbot - carefull- can make crash nginx
        self.setup_certbot_ssl()

        if self.rc.file_exists(pattern = self.certbot_fullchain):
            self.enable_nginx_ssl()
        

        # extra scripts
        self.run_startup_script()

        self.post_deploy()