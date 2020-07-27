from settings import APPS, PROJECT_NAME
from common.deploy import Deployable

class DeployPython(Deployable):

    def __init__(self, app_name, app_stage, params):
        Deployable.__init__(self, stage = app_stage, app_name = app_name, params = params)


    def setup_python_env(self):
        print("\n\n==> setup_python_env\n\n")
        self.rc.chmod(permissions = '+x',
                      pattern     = self.appDir + '/script/setup.sh')
        self.cnx.run('cd {} && \
                     ./script/setup.sh \
                     '.format(self.appDir))


