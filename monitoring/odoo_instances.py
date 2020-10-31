from settings import APPS, APP_STAGES
from fabric_common.common.deploy_python import DeployPython

class Odoo(DeployPython):

    def __init__(self, app_name, stage_name, params):

        """
        DeployPython.__init__(self, 
                            app_stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)

        self.ODOO_PORT 	    = self.port
        self.ODOO_CHAT_PORT = str(int(self.port) + 1)
        #TEMPLATE_LONGPOLLING_PORT
        """

