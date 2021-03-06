from settings import APPS, APP_STAGES
from fabric_common.common.deploy_python import DeployPython

from patchwork.files import directory, exists

from sh import ls, rsync, sshpass


from sh_common.common.utils import log, logi
from sh_common.odoo.odoo import release_path, _pull_release

class IotBox(DeployPython):

    def __init__(self, ssh, app_name, stage_name, params):


        APP_STAGES[app_name][stage_name]['host'] = params.get('host')

        DeployPython.__init__(self, 
                            app_stage = APP_STAGES[app_name][stage_name], 
                            app_name = app_name,
                            params = params)


        self.ODOO_POS_VERSION = "14.0"
        """

        """
        ODOOD_PATH = '/home/odood/'
        self.rc.mkdir(path = ODOOD_PATH)
        self.rc.chmod(permissions = "777", pattern=ODOOD_PATH)

        self.params = params
        self.host   = self.cluster.get('host')#params.get('host')
        self.ssh_login  = self.cluster.get('login')#params.get('user')
        self.ssh_passwd = self.cluster.get('password')#params.get('password')

    def setup_postgresql(self):
        self.db.create_role(role = self.ssh_login)


    # sshpass -p "password" rsync -avz ./deploy/fabric_common/templates/posbox/* deploy@localhost:/srv/http/iotbox-prod/posbox
    # https://stackoverflow.com/questions/3299951/how-to-pass-password-automatically-for-rsync-ssh-command
    def setup_template(self):
        """ 

        """

        r = sshpass("-p", self.ssh_passwd, "rsync","-avz", "./fabric_common/templates/posbox/", 'deploy@{}:{}'.format(self.host, self.appDir)  )
        logi(title="envoie via ssh des templates",msg=r)



        if not exists(self.cnx, self.appDir + '/odoo_src'):
            path_release = _pull_release(release = self.ODOO_POS_VERSION)

            r = sshpass("-p", self.ssh_passwd, "rsync","-avz", path_release, 'deploy@{}:{}'.format(self.host, self.appDir)  )
            logi(title="envoie via ssh de l'instance des sources odoo",msg=r)

            self.cnx.run('cd {} && unzip {}.zip && mkdir odoo_src && mv odoo-{}/* odoo_src && rm -rf odoo-{} && rm {}.zip'.format(self.appDir, self.ODOO_POS_VERSION, self.ODOO_POS_VERSION, self.ODOO_POS_VERSION, self.ODOO_POS_VERSION))





    # https://github.com/odoo/odoo/blob/13.0/addons/point_of_sale/tools/posbox/overwrite_before_init/etc/init_posbox_image.sh
    # https://github.com/odoo/odoo/blob/13.0/addons/point_of_sale/tools/posbox/posbox_create_image.sh


    def setup_git_env(self):
        print("\n\n==> setup_git_env\n\n")

        SRC_DIR = 'odoo_src'

        if not exists(self.cnx, self.appDir + '/' + SRC_DIR + '/.git'):
            #self.cnx.run('cd {} && git clone -b 13.0 --no-local --no-checkout --depth 1 https://github.com/odoo/odoo.git "{}"'.format(self.appDir, SRC_DIR))
            self.cnx.run('cd {} && git clone -b 13.0 --depth 1 https://github.com/odoo/odoo.git "{}"'.format(self.appDir, SRC_DIR))
        else:
            print("GIT repository already exists")

        #self.cnx.run('cd {} && git config core.sparsecheckout true'.format(self.appDir + '/' + SRC_DIR))
        #self.cnx.run('cd {} && echo "addons/web addons/hw_* addons/point_of_sale/tools/posbox/configuration odoo/ odoo-bin" | tee --append .git/info/sparse-checkout > /dev/null'.format(self.appDir + '/' + SRC_DIR))
        #self.cnx.run('cd {} && git read-tree -mu HEAD'.format(self.appDir + '/' + SRC_DIR))






    
    def deploy(self):

        self.pre_deploy()

        # setup
        self.setup_template()
        #self.setup_git_env()


        # update node env
        self.setup_python_env()


        # db
        self.setup_postgresql()





        #self.post_deploy()