from settings import APPS, APP_STAGES
from common.deploy import Deployable

class Static(Deployable):

    def __init__(self, app_name, stage_name, params):
        Deployable.__init__(self, 
                            stage = APP_STAGES[stage_name], 
                            app_name = app_name,
                            params = params)  

    def deploy(self):
        self.pre_deploy()

        print("salut")
        
        
        self.post_deploy()