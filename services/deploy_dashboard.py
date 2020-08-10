from settings import APPS, DASHBOARD_STAGES
from common.deploy import Deployable

class Dashboard(Deployable):

    def __init__(self, stage_name, params):
        Deployable.__init__(self, 
                            stage = DASHBOARD_STAGES[stage_name], 
                            app_name = 'dashboard',
                            params = params)

    def setup_node_env(self):
        print("==> setup_node_env")
        self.rc.chmod(permissions = '+x',
                      pattern     = self.appDir + '/script/setup.sh')
        self.cnx.run('cd {} && \
                     ./script/setup.sh \
                     '.format(self.appDir))

    def build_node_app(self):
        print("==> build_node_app")
        self.cnx.run('cd {}/project && \
                      npm run build \
                     '.format(self.appDir))



    def update_nginx_template(self):
        print("==> config_nginx_template")
        MYHOST = self.stage['host']
        NGINX_FILENAME = self.nginx_filename
        WORKINGDIR = self.appDir + '/project/dist/'

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
        self.rc.copy(src    = self.appDir + '/deploy/archlinux/biachara.dashboard-stage',
                     target = self.nginx_available)

        self.update_nginx_template()


    def enable_nginx_ssl(self):
        print("==> enable_nginx_ssl")
        # enable them
        self.rc.copy(src    = self.appDir + '/deploy/archlinux/biachara.dashboard-stage-ssl',
                     target = self.nginx_available)

        self.update_nginx_template()




    def deploy(self):
        self.pre_deploy()

        #self.manager.executepg(statement = 'CREATE DATABASE {};'.format('coucou3'))#RemotePgsql(conn = self.cnx)
        #self.manager.executepg(statement = 'GRANT ALL PRIVILEGES ON DATABASE datamanager_db TO datamanager;')

        #self.pg.create_db('coucou')

        # setup
        self.setup_git_env()
        # update node env
        self.setup_node_env()
        # build
        self.build_node_app()

        # nginx
        self.config_nginx_template()

        #cerbot - carefull- can make crash nginx

        self.setup_certbot_ssl()

        if self.rc.file_exists(pattern = self.certbot_fullchain):
            self.enable_nginx_ssl()



        self.post_deploy()



