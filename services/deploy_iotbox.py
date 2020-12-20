from settings import APPS, APP_STAGES
from fabric_common.common.deploy_python import DeployPython

class IotBox(DeployPython):

    def __init__(self, ssh, app_name, stage_name, params):


        APP_STAGES[app_name][stage_name]['host'] = params.get('host')

        DeployPython.__init__(self, 
                            app_stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)
        """

        """











    
    def deploy(self):

        """

        """

        self.rc.run('ls -al')