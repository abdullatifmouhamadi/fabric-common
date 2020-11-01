from settings import APPS, APP_STAGES
from fabric_common.common.deploy_python import DeployPython
from odoo.instances import ODOO_INSTANCE_STAGES



class OdooInstances(DeployPython):

    def __init__(self, app_name, stage_name, params):

        DeployPython.__init__(self, 
                            app_stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)


        self.instance        = params.get('instance')
        self.instance_dbname = self.instance+'_'+stage_name
        self.ODOO_PORT 	     = self.port


        self.backend_host        = ODOO_INSTANCE_STAGES[self.instance][stage_name]['backend']
        self.ODOO_CHAT_PORT      = ODOO_INSTANCE_STAGES[self.instance][stage_name]['odoochat-port']
        self.instance_dbpassword = ODOO_INSTANCE_STAGES[self.instance][stage_name]['db_password']
        

        # OVERRIDE NGINX FILENAME
        self.nginx_filename    = self.nginx_filename + '_' + self.instance
        self.nginx_available   = '{}/{}'.format(self._NGINX_AVAILABLE_BASE, self.nginx_filename)
        self.nginx_enabled     = '{}/{}'.format(self._NGINX_ENABLED_BASE, self.nginx_filename)

        # certbot
        self.certbot_fullchain = '/etc/letsencrypt/live/'+self.backend_host+'/fullchain.pem'



    # not working -> exists doesn'- work (i suspect it works only if the 'deploy' user own the file)
    def setup_certbot_ssl(self):
        if (self.params['certbot'] == False):
            return False
        
        print("\n\n==> setup_certbot_ssl\n\n")
        if not self.rc.file_exists(pattern = self.certbot_fullchain): # create them
            self.rc.certbot(param = self.backend_host +',www.' + self.backend_host)
            return False
        else:
            return True




    def update_nginx_template(self):

        MYHOST           = self.backend_host
        NGINX_FILENAME   = self.nginx_filename
        HEADER_DB_FILTER = self.instance+'_'


        self.rc.sed(self.nginx_available, 'MYHOST', MYHOST)
        self.rc.sed(self.nginx_available, 'NGINX_FILENAME', NGINX_FILENAME)
        self.rc.sed(self.nginx_available, 'ODOO_PORT', self.ODOO_PORT)
        self.rc.sed(self.nginx_available, 'ODOO_CHAT_PORT', self.ODOO_CHAT_PORT)
        self.rc.sed(self.nginx_available, 'HEADER_DB_FILTER', HEADER_DB_FILTER)

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


    def install_database(self):
        print("\n\n==> install_database\n\n")

        # https://www.odoo.com/fr_FR/forum/aide-1/question/creating-db-template-and-deploying-to-new-db-how-to-111933
        # odoo-bin -c ../deploy/odoo.conf -d 'maoredev_dev' --without-demo=all
        # odoo-bin -r 'odoo_maoredev_business_dev' -w 'mayottePass976' -d 'maoredev_dev' --without-demo=all
        # ./odoo-bin -r 'odoo_maoredev_business_dev' -w 'mayottePass976' -i base -d 'maoredev_dev' --without-demo=all --stop-after-init



        if (self.rc.db_exists(dbname=self.instance_dbname)):
            print("\n\n==> bdd existe déjà")
        else:
            self.setup_database_and_access( dbname=self.instance_dbname, 
                                            username=self.pgdb_username, 
                                            password=self.instance_dbpassword)

            self.db.assign_owner(dbname=self.instance_dbname, owner=self.pgdb_username)

            # initiate db
            self.rc.run("cd {} && ../venv/bin/python3.6 ../odoo_src/odoo-bin -r '{}' -w '{}' -i base -d '{}' --without-demo=all --stop-after-init".format(self.appDir+'/odoo_src/', self.pgdb_username, self.instance_dbpassword, self.instance_dbname))




    
    def instantiate(self):
        print("\n\n==> instance = " + self.instance_dbname + '\n\n')



        self.install_database()


