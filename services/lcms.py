

from ..common.build import Build
from ..core.latex import Latex
from ..core.csv_simple import CSVSimple



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





    def parse_pedagogie(self, path):
        obj         = CSVSimple(path=path)
        data        = obj.pd

        row_count   = sum(1 for row in data.iterrows())
        max_group   = max(data['group'])
        pedagogies  = []
        modules     = {}
        sequences   = []
        
        for group in range(max_group+1):
            modules = {}
            sequences = []
            for index in range(row_count):
                row = data.iloc[index]
                if group == row['group']:
                    if isinstance(row['module_dossier'], str):
                        modules = {
                        'module_dossier':row['module_dossier'].replace("'",""),
                        'module_titre':row['module_titre'],
                        'module_slogan':row['module_slogan'],
                        'module_objectif_professionnel':row['module_objectif_professionnel'],
                        'module_objectif_examen':row['module_objectif_examen'],
                        'module_template_prerequis':row['module_template_prerequis'],
                        'module_template_pedagogie':row['module_template_pedagogie'],
                        'module_template_conducteur':row['module_template_conducteur'],
                        'module_template_poster':row['module_template_poster'].replace("'",""),
                        }
                    sequences.append({
                        'sequence_titre':row['sequence_titre'],
                        'sequence_objectif':row['sequence_objectif'],
                        'sequence_taxonomie':row['sequence_taxonomie'],
                        'sequence_duree_theorie':row['sequence_duree_theorie'],
                        'sequence_duree_pratique':row['sequence_duree_pratique'],
                        'sequence_template_referentiel':row['sequence_template_referentiel'],
                    })
            if len(modules)>0:
                modules['sequences']=sequences
                pedagogies.append(modules)
                #pprint(modules)
            
        return pedagogies