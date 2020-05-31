

from ..common.build import Build
from ..core.latex import Latex

class LearningContentManagementSystem():
    def __init__(self, ssh, app, discipline, category, id):
        
        """
        construct
        """
        ##
        self.ssh = ssh
        self.bash = ssh.bash

        ##
        self.app = app
        self.discipline = discipline
        self.category = category
        self.id = id 

        ##
        self.latex = Latex(ssh=ssh)




        ## DIRS
        self.disciplineDir = self.app['build_dir'] + '/' + self.discipline
        self.categoryDir   = self.disciplineDir + '/' + self.category
        self.idDir         = self.categoryDir + '/' + self.id


        ##
        self.setup()



    def setup(self):

        self.bash.mkdir(self.disciplineDir)
        self.bash.mkdir(self.categoryDir)

        self.bash.remove(self.idDir)
        self.bash.mkdir(self.idDir)
        

    
    


    def compile(self, src):



        return self.latex.compile(path = self.app['src_dir'], src=src)



    def build(self):
        """
            préeliminaires
        """

        build = Build(bash      = self.bash, 
                      src_dir   = self.app['src_dir'], 
                      build_dir = self.app['build_dir'], 
                      repo      = self.app['repo'], 
                      branch    = self.app['branch'],
                      owner     = self.ssh.ssh_user)


        #self.bash.pwd()
        #self.bash.directory_exists(pattern='/d')





