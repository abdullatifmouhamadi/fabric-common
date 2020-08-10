from settings import APPS, DATAMANAGER_STAGES, PROJECT_NAME
from common.deploy_django import DeployDjango

class Datamanager(DeployDjango):

    def __init__(self, stage_name, params):
        DeployDjango.__init__(self, app_name = 'datamanager', app_stage = DATAMANAGER_STAGES[stage_name], params = params)
        self.current_stage_name = stage_name

    def update_nginx_template(self):
        MYPORT = '80' #self.port
        MYHOST = self.stage['host']
        MYSOCKET = self.appDir + '/src/project/datamanager.sock'
        NGINX_FILENAME = self.nginx_filename
        MEDIA_PATH = self.appDir + '/src/project/media'
        STATIC_PATH = self.appDir + '/src/project/static'
        UPSTREAM_NAME = PROJECT_NAME + '_' + self.app['name'] + '_' + self.stage['name']
        UWSGI_PARAM_PATH = self.appDir + '/src/project/project/uwsgi_params'

        self.rc.sed(self.nginx_available, 'MYHOST', MYHOST)
        self.rc.sed(self.nginx_available, 'NGINX_FILENAME', NGINX_FILENAME)
        self.rc.sed(self.nginx_available, 'MYPORT', MYPORT)
        self.rc.sed(self.nginx_available, 'UPSTREAM_NAME', UPSTREAM_NAME)

        self.rc.sed(self.nginx_available, 'MYSOCKET', MYSOCKET.replace('/', r'\/'))
        self.rc.sed(self.nginx_available, 'MEDIA_PATH', MEDIA_PATH.replace('/', r'\/'))
        self.rc.sed(self.nginx_available, 'STATIC_PATH', STATIC_PATH.replace('/', r'\/'))
        self.rc.sed(self.nginx_available, 'UWSGI_PARAM_PATH', UWSGI_PARAM_PATH.replace('/', r'\/'))

        # link
        self.rc.linksoft(self.nginx_available, self.nginx_enabled)

        # reload nginx
        self.rc.reloadnginx()


    def config_nginx_template(self):
        print("\n\n==> config_nginx_template\n\n")
        self.rc.copy(src    = self.appDir + '/deploy/archlinux/biachara.datamanager-nginx',
                     target = self.nginx_available)

        self.update_nginx_template()

    def enable_nginx_ssl(self):
        print("\n\n==> enable_nginx_ssl\n\n")
        # enable them
        self.rc.copy(src    = self.appDir + '/deploy/archlinux/biachara.datamanager-nginx-ssl',
                     target = self.nginx_available)

        self.update_nginx_template()


    def config_systemd_template(self):
        print("\n\n==> config_systemd_template\n\n")

        self.rc.stopdaemon(service = self.daemon_filename)

        DESCRIPTION = "Biachara datamanager s instance : {}".format(self.daemon_filename)
        MYWORKING_DIRECTORY = self.appDir + '/deploy/'
        EXEC_FILE = self.appDir + '/deploy/run_datamanager.sh'

        self.rc.copy(src    = self.appDir + '/deploy/archlinux/biachara.datamanager.service',
                     target = self.daemon_location)

        self.rc.sed(self.daemon_location, 'DESCRIPTION', DESCRIPTION)
        self.rc.sed(self.daemon_location, 'MYWORKING_DIRECTORY', MYWORKING_DIRECTORY.replace('/', r'\/'))
        self.rc.sed(self.daemon_location, 'EXEC_FILE', EXEC_FILE.replace('/', r'\/'))

        self.rc.daemonreload()
        self.rc.startdaemon(service = self.daemon_filename)


    def config_scraping_service(self):
        print("\n\n==> config_scraping_service\n\n")


        from settings import SCRAPING_STAGES, SCRAPING_STAGES
        scraping_port_prefix = APPS['scraping']['port_prefix']
        scraping_port_suffix = SCRAPING_STAGES[self.current_stage_name]['port_suffix']
        scraping_port = scraping_port_prefix + scraping_port_suffix
        MYBIACHARACLUSTER = 'http://localhost:' + scraping_port
        self.rc.sed(self.biachara_conf_file, 'MYBIACHARACLUSTER', MYBIACHARACLUSTER.replace('/', r'\/'))



    def deploy(self):
        self.pre_deploy()
        # setup
        self.setup_git_env()

        # db
        self.config_database_conf_file()
        self.setup_database()


        # stop daemon 
        print("\n\n==> stopping daemon ...\n\n")
        self.rc.stopdaemon(service = self.daemon_filename)

        # update node env
        self.setup_python_env()
        self.setup_django_env()
        self.setup_django_settings()

        # biachara
        self.config_scraping_service()

        # celery
        self.setup_celery()

        # systemd
        self.config_systemd_template()

        # nginx
        self.config_nginx_template()

        #cerbot - carefull- can make crash nginx
        self.setup_certbot_ssl()

        if self.rc.file_exists(pattern = self.certbot_fullchain):
            self.enable_nginx_ssl()

        self.post_deploy()
