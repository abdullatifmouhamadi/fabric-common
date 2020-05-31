

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

        ##
        self.setup()



    def setup(self):
        DISCIPLINE_DIR = self.app['build_dir'] + '/' + self.discipline
        CATEGORY_DIR   = DISCIPLINE_DIR + '/' + self.category
        ID_DIR         = CATEGORY_DIR + '/' + self.id

        self.bash.mkdir(DISCIPLINE_DIR)
        self.bash.mkdir(CATEGORY_DIR)

        self.bash.remove(ID_DIR)
        self.bash.mkdir(ID_DIR)
        

    
    


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





