from settings import APPS, APP_STAGES
from fabric_common.common.deploy_python import DeployPython

class Odoo(DeployPython):

    def __init__(self, app_name, stage_name, params):
        DeployPython.__init__(self, 
                            app_stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)

        self.ODOO_PORT 	    = self.port
        self.ODOO_CHAT_PORT = str(int(self.port) + 1)



    def config_systemd_template(self):
        print("\n\n==> config_systemd_template\n\n")

        self.rc.stopdaemon(service = self.daemon_filename)

        DESCRIPTION = "Odoo deamon : {}".format(self.daemon_filename)
        MYWORKING_DIRECTORY = self.appDir + '/deploy/'
        EXEC_FILE = self.appDir + '/deploy/run.sh'

        self.rc.sed(self.appDir + '/deploy/run.sh', 'MYPORT', self.ODOO_PORT)

        self.rc.copy(src    = self.appDir + '/deploy/archlinux/template-systemd.service',
                     target = self.daemon_location)

        self.rc.sed(self.daemon_location, 'DESCRIPTION', DESCRIPTION)
        self.rc.sed(self.daemon_location, 'MYWORKING_DIRECTORY', MYWORKING_DIRECTORY.replace('/', r'\/'))
        self.rc.sed(self.daemon_location, 'EXEC_FILE', EXEC_FILE.replace('/', r'\/'))

        self.rc.daemonreload()
        self.rc.startdaemon(service = self.daemon_filename)





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

        

        # systemd
        self.config_systemd_template()
        

        
        #cerbot - carefull- can make crash nginx
        self.setup_certbot_ssl()

        if self.rc.file_exists(pattern = self.certbot_fullchain):
            self.enable_nginx_ssl()
        


        self.post_deploy()
