import pandas as pd



class CSVSimple:
  def __init__(self, path):
    self.path = path
    self.pd   = pd.read_csv(self.path, sep=';', index_col=0)


  def test(self):
    for index, row in self.pd.iterrows():

      print(row['module_dossier'])


      