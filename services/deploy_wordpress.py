from settings import APPS, APP_STAGES
from fabric_common.common.deploy import Deployable



class Wordpress(Deployable):

    def __init__(self, app_name, stage_name, params):
        Deployable.__init__(self, 
                            stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)



        self.rc.mkdir(path   ='/home/wordpressd/')
        self.rc.sudo(command = 'chmod -R 777 /home/wordpressd/')

    def install_prestashop(self):
        SCRIPT_PATH = self.appDir + '/script/'
        APP_PATH    = self.appDir + '/src/wordpress/'
        self.rc.run("cd {} && python setup.py".format(SCRIPT_PATH))
        self.rc.sudo("chmod -R 755 {}".format(APP_PATH))


    def setup_script_templates(self):
        print("\n\n==> setup_script_templates\n\n")
        #setup.py

        TEMPLATE_CMS_DB_NAME     = 'wordpress_'+self.stage['host']
        self.rc.sed(self.appDir + '/script/setup.py', 'TEMPLATE_CMS_DB_NAME', TEMPLATE_CMS_DB_NAME)

        ##


    def deploy(self):
        self.pre_deploy()

        # setup
        self.setup_git_env()

        # template scripts
        self.setup_script_templates()

        #
        self.install_prestashop()

        #cerbot - carefull- can make crash nginx
        self.setup_certbot_ssl()

        if self.rc.file_exists(pattern = self.certbot_fullchain):
            self.enable_nginx_ssl()
        
        self.post_deploy()