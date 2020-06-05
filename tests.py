
from core.csv_simple import CSVSimple



def csv_test():
    print("hello world!")

    obj = CSVSimple(path='./tests/csv_pedagogie.csv')
    
    #print(obj.pd)
    #obj.test()




    #obj.pd['module_dossier'] = obj.pd['module_dossier'].astype(str)
    #obj.pd = obj.pd.applymap(str)
    for index, row in obj.pd.iterrows():

        

      print(row['module_dossier'])



if __name__ == "__main__":
    csv_test()


