

from ..common.build import Build
from ..core.latex import Latex
from ..core.csv_simple import CSVSimple
from pprint import pprint
from pandas import DataFrame
import pandas as pd
import time 




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


        ## PEDAGOGIE PARSING
        self.pedagogies = None

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



    def get_pedagogie_module(self, module_dossier):
        for pedagogie in self.pedagogies:
            if pedagogie['module_dossier'] == module_dossier:
                return pedagogie
        return None




    def process_duree_totale(self, module_dossier):
        pedagogie            = self.get_pedagogie_module(module_dossier = module_dossier)
        sequences            = pedagogie['sequences'] 
        total_duree_theorie  = 0
        total_duree_pratique = 0
        for sequence in sequences:
            total_duree_theorie += int(sequence['sequence_duree_theorie'])
            total_duree_pratique += int(sequence['sequence_duree_pratique'])
        return total_duree_theorie + total_duree_pratique


    def formatTime(self, seconds): 
        min, sec = divmod(seconds, 60) 
        hour, min = divmod(min, 60) 
        return "%dh%02d" % (hour, min) # "%d:%02d:%02d" % (hour, min, sec) 

    def generate_suivi_pedagogique_list(self, output):
        csv                  = []
        pos                  = 0
        total_duree_theorie  = 0
        total_duree_pratique = 0
        csv.append({
            'col0':'#',
            'col1':'module',
            'col2':'sequence',
            'col3':'taxonomie',
            'col4':'theorie',
            'col5':'pratique',
        })
        for pedagogie in self.pedagogies:
            sequences = pedagogie['sequences']
            for sequence in sequences:
                pos = pos + 1
                csv.append({
                    'col0':pos,
                    'col1':str(pedagogie['module_titre']),
                    'col2':str(sequence['sequence_titre']),
                    'col3':str(sequence['sequence_taxonomie']),
                    'col4':str(sequence['sequence_duree_theorie']) +'min',
                    'col5':str(sequence['sequence_duree_pratique']) +'min',
                })
                total_duree_theorie += int(sequence['sequence_duree_theorie'])
                total_duree_pratique += int(sequence['sequence_duree_pratique'])

        #pprint(self.formatTime(total_duree_pratique * 60))

        csv.append({
            'col0':"-",
            'col1':"\\bfseries Total",
            'col2':"-",
            'col3':"-",
            'col4':"\\bfseries " + self.formatTime(total_duree_theorie * 60),
            'col5':"\\bfseries " + self.formatTime(total_duree_pratique * 60),
        })
        df = pd.DataFrame(csv)
        df.to_csv( output , index = False, sep=',', header=False)
        return None



    def generate_sequence_list(self, module_dossier, output):
        pedagogie            = self.get_pedagogie_module(module_dossier = module_dossier)
        sequences            = pedagogie['sequences']
        csv                  = []
        pos                  = 0
        total_duree_theorie  = 0
        total_duree_pratique = 0

        csv.append({
            'col0':'#',
            'col1':'Titre de la sequence',
            'col2':'theorie',
            'col3':'pratique',
        })
        for sequence in sequences:
            pos = pos + 1
            csv.append({
                'col0':pos,
                'col1':str(sequence['sequence_titre']),
                'col2':str(sequence['sequence_duree_theorie']) +'min',
                'col3':str(sequence['sequence_duree_pratique']) +'min',
            })
            total_duree_theorie += int(sequence['sequence_duree_theorie'])
            total_duree_pratique += int(sequence['sequence_duree_pratique'])

        csv.append({
            'col0':"-",
            'col1':"\\bfseries Total",
            'col2':"\\bfseries " + self.formatTime(total_duree_theorie * 60),
            'col3':"\\bfseries " + self.formatTime(total_duree_pratique * 60),
        })
        df = pd.DataFrame(csv)
        df.to_csv( output , index = False, sep=';', header=False)





    def parse_pedagogie(self, path):
        obj         = CSVSimple(path=path)
        data        = obj.pd

        row_count   = sum(1 for row in data.iterrows())
        max_group   = max(data['group'])
        self.pedagogies  = []
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
                self.pedagogies.append(modules)
                #pprint(modules)
            
        return self.pedagogies