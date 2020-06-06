
from core.csv_simple import CSVSimple
import math
from pprint import pprint

def csv_test():
    print("hello world!")

    obj = CSVSimple(path='./tests/csv_pedagogie.csv')
    
    #print(obj.pd)
    #obj.test()

    #obj.pd['module_dossier'] = obj.pd['module_dossier'].astype(str)
    #obj.pd = obj.pd.applymap(str)
    sequences = []
    sequence_obj = []
    index_dy = 1
    for index, row in obj.pd.iterrows():

      module_dossier = row['module_dossier']

      sequence_obj.append ({
        'sequence_titre':row['sequence_titre'],
      })

      #if isinstance(module_dossier, str):
      #  pprint(sequence_obj)

      if index > index_dy:
        index_dy = index
        #sequence_obj = []
        #print(index_dy)


      print(index)


      if isinstance(module_dossier, str):
        #pprint(sequence_obj)
        module_dossier = module_dossier.replace("'",'')

        sequences.append({'module_dossier':module_dossier,
                          'module_title':row['module_titre'],
                          'sequences':sequence_obj})
        
        sequence_obj = []

        


      #pprint(math.isnan(index))




      #if isinstance()
      #print( math.isnan(row['module_dossier']) )
      #if row['module_dossier'] == np.nan:
      #  print("nand")

    #pprint(sequences)


if __name__ == "__main__":
    csv_test()


