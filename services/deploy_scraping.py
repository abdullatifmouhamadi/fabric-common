from settings import APPS, SCRAPING_STAGES, PROJECT_NAME
from common.deploy_django import DeployDjango

class Scraping(DeployDjango):

    def __init__(self, stage_name, params):
        DeployDjango.__init__(self, app_name = 'scraping', app_stage = SCRAPING_STAGES[stage_name], params = params)

        self.scrapydconf_filename = self.appDir + '/src/project/app_scrapyd/scrapyd.conf'
        self.scrapyd_run_filename = self.appDir + '/deploy/run_scrapyd.sh'

    def setup_scrapyd_conf(self):
        BIND_ADDRESS = 'localhost'
        HTTP_PORT    = self.port
        self.rc.sed(self.scrapydconf_filename, 'BIND_ADDRESS', BIND_ADDRESS)
        self.rc.sed(self.scrapydconf_filename, 'HTTP_PORT', HTTP_PORT)

    def config_scrapyd_run(self):
        APPDIR = self.appDir
        self.rc.sed(self.scrapyd_run_filename, 'APPDIR', APPDIR.replace('/', r'\/'))

    def config_systemd_template(self):
        print("==> config_systemd_template")

        self.rc.stopdaemon(service = self.daemon_filename)

        DESCRIPTION         = "Biachara scraping s instance : {}".format(self.daemon_filename)
        MYWORKING_DIRECTORY = self.appDir + '/src/project/app_scrapyd/'
        EXEC_FILE           = self.scrapyd_run_filename#self.appDir + '/deploy/run_scrapyd.sh'

        self.rc.copy(src    = self.appDir + '/deploy/archlinux/biachara.scraping-stage.service',
                     target = self.daemon_location)

        self.rc.sed(self.daemon_location, 'DESCRIPTION', DESCRIPTION)
        self.rc.sed(self.daemon_location, 'MYWORKING_DIRECTORY', MYWORKING_DIRECTORY.replace('/', r'\/'))
        self.rc.sed(self.daemon_location, 'EXEC_FILE', EXEC_FILE.replace('/', r'\/'))

        self.rc.daemonreload()

        self.rc.startdaemon(service = self.daemon_filename)



    def deploy(self):
        self.pre_deploy()
        # setup
        self.setup_git_env()

        # db
        self.config_database_conf_file()
        self.setup_database()

        # update node env
        self.setup_python_env()
        self.setup_django_env()
        #self.setup_django_settings()

        # scrapyd
        self.setup_scrapyd_conf()
        self.config_scrapyd_run()
        # systemd
        self.config_systemd_template()
        """
        # nginx
        self.config_nginx_template()

        #cerbot - carefull- can make crash nginx
        self.setup_certbot_ssl()

        if self.rc.file_exists(pattern = self.certbot_fullchain):
            self.enable_nginx_ssl()

        """


        self.post_deploy()