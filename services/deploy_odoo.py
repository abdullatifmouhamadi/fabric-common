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

        self.ODOO_UPSTREAM      = 'odoo-'+self.project_key + '-' + self.app['name'] + '-' + self.stage['name'] + '-upstream'
        self.ODOO_CHAT_UPSTREAM = 'odoo-chat-'+self.project_key + '-' + self.app['name'] + '-' + self.stage['name'] + '-upstream'

        #TEMPLATE_LONGPOLLING_PORT

    def update_nginx_template(self):
        
        #ODOO_CHAT_PORT = '8072' # bricolage

        #MYPORT = '80' #self.port
        MYHOST = self.stage['host']
        #MYSOCKET = self.appDir + '/src/project/datamanager.sock'
        NGINX_FILENAME = self.nginx_filename
        #MEDIA_PATH = self.appDir + '/src/project/media'
        #STATIC_PATH = self.appDir + '/src/project/static'
        #UPSTREAM_NAME = PROJECT_NAME + '_' + self.app['name'] + '_' + self.stage['name']
        #UWSGI_PARAM_PATH = self.appDir + '/src/project/project/uwsgi_params'

        self.rc.sed(self.nginx_available, 'MYHOST', MYHOST)
        self.rc.sed(self.nginx_available, 'NGINX_FILENAME', NGINX_FILENAME)
        #self.rc.sed(self.nginx_available, 'MYPORT', MYPORT)
        self.rc.sed(self.nginx_available, 'ODOO_PORT', self.ODOO_PORT)
        self.rc.sed(self.nginx_available, 'ODOO_CHAT_PORT', self.ODOO_CHAT_PORT)
        self.rc.sed(self.nginx_available, 'ODOO_UPSTREAM', self.ODOO_UPSTREAM)
        self.rc.sed(self.nginx_available, 'ODOO_CHAT_UPSTREAM', self.ODOO_CHAT_UPSTREAM)

        #self.rc.sed(self.nginx_available, 'MEDIA_PATH', MEDIA_PATH.replace('/', r'\/'))
        #self.rc.sed(self.nginx_available, 'STATIC_PATH', STATIC_PATH.replace('/', r'\/'))
        #self.rc.sed(self.nginx_available, 'UWSGI_PARAM_PATH', UWSGI_PARAM_PATH.replace('/', r'\/'))

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
        TEMPLATE_ROLE_NAME        = self.pgdb_username
        TEMPLATE_LONGPOLLING_PORT = self.ODOO_CHAT_PORT
        TEAMPLATE_DB_FILTER       = self.stage['name']
        #print(TEMPLATE_ROLE_NAME)

        self.rc.sed(self.appDir + '/deploy/odoo.conf', 'TEMPLATE_ROLE_NAME', TEMPLATE_ROLE_NAME)
        self.rc.sed(self.appDir + '/deploy/odoo.conf', 'TEMPLATE_LONGPOLLING_PORT', TEMPLATE_LONGPOLLING_PORT)
        self.rc.sed(self.appDir + '/deploy/odoo.conf', 'TEAMPLATE_DB_FILTER', TEAMPLATE_DB_FILTER)
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

        # nginx
        self.config_nginx_template()

        #cerbot - carefull- can make crash nginx
        self.setup_certbot_ssl()

        if self.rc.file_exists(pattern = self.certbot_fullchain):
            self.enable_nginx_ssl()
        


        self.post_deploy()
