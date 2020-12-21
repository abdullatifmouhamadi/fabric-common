from settings import APPS, APP_STAGES
from fabric_common.common.deploy_python import DeployPython

from patchwork.files import directory, exists

class IotBox(DeployPython):

    def __init__(self, ssh, app_name, stage_name, params):


        APP_STAGES[app_name][stage_name]['host'] = params.get('host')

        DeployPython.__init__(self, 
                            app_stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)
        """

        """




    def setup_git_env(self):
        print("\n\n==> setup_git_env\n\n")

        if not exists(self.cnx, self.appDir + '/.git'):
            self.cnx.run('cd {} && git clone -b 9.0 --no-checkout --depth 1 https://github.com/odoo/odoo.git'.format(self.appDir))

            self.cnx.run('cd {} && git config core.sparsecheckout true echo "addons/web addons/web_kanban addons/hw_* addons/point_of_sale/tools/posbox/configuration openerp/ odoo.py" | tee --append .git/info/sparse-checkout > /dev/null'.format(self.appDir + '/odoo'))
            self.cnx.run('cd {} && git read-tree -mu HEAD'.format(self.appDir + '/odoo'))

        else:
            print("GIT repository already exists")








    
    def deploy(self):

        self.pre_deploy()

        # setup
        self.setup_git_env()










        self.post_deploy()