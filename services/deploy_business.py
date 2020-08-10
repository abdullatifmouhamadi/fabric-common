from settings import APPS, BUSINESS_STAGES, PROJECT_NAME
from common.deploy_python import DeployPython

class Business(DeployPython):

    def __init__(self, stage_name, params):
        DeployPython.__init__(self, app_name = 'business', app_stage = BUSINESS_STAGES[stage_name], params = params)
        self.current_stage_name = stage_name

        self.ODOO_PORT 	   = self.port

    def update_nginx_template(self):
        
        ODOO_CHAT_PORT = '8072' # bricolage

        MYPORT = '80' #self.port
        MYHOST = self.stage['host']
        #MYSOCKET = self.appDir + '/src/project/datamanager.sock'
        NGINX_FILENAME = self.nginx_filename
        #MEDIA_PATH = self.appDir + '/src/project/media'
        #STATIC_PATH = self.appDir + '/src/project/static'
        #UPSTREAM_NAME = PROJECT_NAME + '_' + self.app['name'] + '_' + self.stage['name']
        #UWSGI_PARAM_PATH = self.appDir + '/src/project/project/uwsgi_params'

        self.rc.sed(self.nginx_available, 'MYHOST', MYHOST)
        self.rc.sed(self.nginx_available, 'NGINX_FILENAME', NGINX_FILENAME)
        self.rc.sed(self.nginx_available, 'MYPORT', MYPORT)
        self.rc.sed(self.nginx_available, 'ODOO_PORT', self.ODOO_PORT)
        self.rc.sed(self.nginx_available, 'ODOO_CHAT_PORT', ODOO_CHAT_PORT)
        #self.rc.sed(self.nginx_available, 'UPSTREAM_NAME', UPSTREAM_NAME)

        #self.rc.sed(self.nginx_available, 'MEDIA_PATH', MEDIA_PATH.replace('/', r'\/'))
        #self.rc.sed(self.nginx_available, 'STATIC_PATH', STATIC_PATH.replace('/', r'\/'))
        #self.rc.sed(self.nginx_available, 'UWSGI_PARAM_PATH', UWSGI_PARAM_PATH.replace('/', r'\/'))

        # link
        self.rc.linksoft(self.nginx_available, self.nginx_enabled)

        # reload nginx
        self.rc.reloadnginx()


    def setup_python_env(self):
        print("\n\n==> setup_python_env\n\n")
        self.rc.chmod(permissions = '+x',
                      pattern     = self.appDir + '/odoo/script/setup.sh')
        self.cnx.run('cd {} && \
                     ./script/setup.sh \
                     '.format(self.appDir+'/odoo/'))


    def config_nginx_template(self):
        print("\n\n==> config_nginx_template\n\n")
        self.rc.copy(src    = self.appDir + '/odoo/deploy/archlinux/biachara.business-nginx',
                     target = self.nginx_available)

        self.update_nginx_template()

    def enable_nginx_ssl(self):
        print("\n\n==> enable_nginx_ssl\n\n")
        # enable them
        self.rc.copy(src    = self.appDir + '/odoo/deploy/archlinux/biachara.business-nginx-ssl',
                     target = self.nginx_available)

        self.update_nginx_template()


    def config_systemd_template(self):
        print("\n\n==> config_systemd_template\n\n")

        self.rc.stopdaemon(service = self.daemon_filename)

        DESCRIPTION = "Biachara Business s instance : {}".format(self.daemon_filename)
        MYWORKING_DIRECTORY = self.appDir + '/odoo/deploy/'
        EXEC_FILE = self.appDir + '/odoo/deploy/run.sh'

        self.rc.sed(self.appDir + '/odoo/deploy/run.sh', 'MYPORT', self.ODOO_PORT)

        self.rc.copy(src    = self.appDir + '/odoo/deploy/archlinux/biachara.business.service',
                     target = self.daemon_location)

        self.rc.sed(self.daemon_location, 'DESCRIPTION', DESCRIPTION)
        self.rc.sed(self.daemon_location, 'MYWORKING_DIRECTORY', MYWORKING_DIRECTORY.replace('/', r'\/'))
        self.rc.sed(self.daemon_location, 'EXEC_FILE', EXEC_FILE.replace('/', r'\/'))

        self.rc.daemonreload()
        self.rc.startdaemon(service = self.daemon_filename)


    def setup_database(self):

        DB_NAME = 'odoodev'
        PG_ROLE = 'odoodev'
        PW_ROLE = 'mayottePass976'
        self.db.create_db(dbname     = DB_NAME)
        self.db.create_role(role = PG_ROLE, password=PW_ROLE)
        self.db.grant_all(dbname     = DB_NAME,
                          role       = PG_ROLE)



        


    def deploy(self):
        self.pre_deploy()
        # setup
        self.setup_git_env()

        # db
        #self.config_database_conf_file()
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
