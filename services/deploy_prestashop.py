from settings import APPS, APP_STAGES
from fabric_common.common.deploy import Deployable



class Prestashop(Deployable):

    def __init__(self, app_name, stage_name, params):
        Deployable.__init__(self, 
                            stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)
        





    def install_prestashop(self):
        SCRIPT_PATH = self.appDir + '/script/'


        self.rc.run("cd {} && python setup.py".format(SCRIPT_PATH))
        #self.rc.python('myscript')
        print("salut {}".format(SCRIPT_PATH))



    def deploy(self):
        self.pre_deploy()

        # setup
        #self.setup_git_env()

        self.install_prestashop()



        #self.post_deploy()