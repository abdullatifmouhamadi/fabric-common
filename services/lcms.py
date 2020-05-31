

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
                        code_dir = self.app['code_dir'], 
                        repo = self.app['repo'], 
                        branch = self.app['branch'],
                        owner = self.ssh.ssh_user)


        self.bash.pwd()
        #self.bash.directory_exists(pattern='/d')





