

from ..common.build import Build


class LearningContentManagementSystem():
    def __init__(self, ssh, app, discipline, category, id):
        
        """
        construct
        """

        

        print(app)
        self.ssh = ssh
        self.bash = ssh.bash
        self.app = app











    def build(self):
        """
            préeliminaires
        """

        build = Build(  bash = self.bash, 
                        src_dir = self.app['src_dir'], 
                        build_dir = self.app['build_dir'], 
                        repo = self.app['repo'], 
                        branch = self.app['branch'],
                        owner = self.ssh.ssh_user)


        self.bash.pwd()
        #self.bash.directory_exists(pattern='/d')





