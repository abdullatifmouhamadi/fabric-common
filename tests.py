
from core.csv_simple import CSVSimple
import math
from pprint import pprint

def csv_test():
    print("hello world!")

    obj = CSVSimple(path='./tests/csv_pedagogie.csv')
    data = obj.pd




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
    





if __name__ == "__main__":
    csv_test()


