from settings import APPS, APP_STAGES
from fabric_common.common.deploy_python import DeployPython

class Odoo(DeployPython):

    def __init__(self, app_name, stage_name, params):
        DeployPython.__init__(self, 
                            app_stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)




    def setup_database(self):
        print("\n\n==> setup_database\n\n")
        TEMPLATE_ROLE_NAME = self.pgdb_username
        print(TEMPLATE_ROLE_NAME)

        self.rc.sed(self.appDir + '/deploy/odoo.conf', 'TEMPLATE_ROLE_NAME', TEMPLATE_ROLE_NAME)
        self.rc.sed(self.appDir + '/script/setup.py', 'TEMPLATE_ROLE_NAME', TEMPLATE_ROLE_NAME)

        self.rc.run("cd {} && python setup.py".format(self.appDir + '/script/'))


    def deploy(self):
        self.pre_deploy()

        # setup
        self.setup_git_env()

        self.setup_database()


        # stop daemon 
        print("\n\n==> stopping daemon ...\n\n")
        self.rc.stopdaemon(service = self.daemon_filename)

        # update node env
        self.setup_python_env()

        


        
        #cerbot - carefull- can make crash nginx
        self.setup_certbot_ssl()

        if self.rc.file_exists(pattern = self.certbot_fullchain):
            self.enable_nginx_ssl()
        


        self.post_deploy()