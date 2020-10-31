from settings import APPS, APP_STAGES
from fabric_common.common.deploy_python import DeployPython

class OdooInstances(DeployPython):

    def __init__(self, app_name, stage_name, params):

        DeployPython.__init__(self, 
                            app_stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)

        self.instance        = params.get('instance')
        self.instance_dbname = self.instance
        """
        self.ODOO_PORT 	    = self.port
        self.ODOO_CHAT_PORT = str(int(self.port) + 1)
        #TEMPLATE_LONGPOLLING_PORT
        """



    def update_nginx_template(self):
        """

        """

    def config_nginx_template(self):
        print("\n\n==> config_nginx_template\n\n")
        """

        """

    def enable_nginx_ssl(self):
        print("\n\n==> enable_nginx_ssl\n\n")


    def install_database(self):
        print("\n\n==> install_database\n\n")

    
    def instantiate(self):
        print("instance = " + self.instance_dbname )