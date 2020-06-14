from fabric_common.common.build import Build

class Device:
    def __init__(self, ssh, app):
        """
        Build construct
        """
        ##
        self.ssh        = ssh
        self.bash       = ssh.bash
        self.app        = app
        self.installDir = app['install_dir']

        self.pre_build()



    def pre_build(self):
        self.bash.mkdir(self.installDir)
        self.bash.chown(owner   = '{}:wheel'.format(self.ssh.ssh_user), pattern = self.installDir)




    def setup(self):
        """
        Préeliminaires
        """
        Build(bash      = self.bash, 
              src_dir   = self.app['src_dir'], 
              build_dir = self.app['build_dir'], 
              repo      = self.app['repo'], 
              branch    = self.app['branch'],
              owner     = self.ssh.ssh_user)

