import pickle

import parser_module
from  parser_module import  Parse
import search_engine
import numpy
import pandas as pd
from reader import ReadFile

if __name__ == '__main__':
    print( numpy.__version__)
    #df = pd.read_parquet("C:\Users\Admin\Desktop\Data\date=08-07-2020\covid19_08-07.snappy.parquet", engine="pyarrow")
    #print(df[0])
    #r = ReadFile("C:/Users/Admin/Desktop/Data/date=08-07-2020")
    #print(len(r))
    #readfile=r.read_file("covid19_08-07.snappy.parquet")

    # for n in readfile:
    #     num = 0
    #     for l in n:
    #         num+=1
    #         if l!=None:
    #             print(str(num)+") "+l)

    #print("niv is the best git user")
    #print(len(readfile))
    #Parse.__init__(parser_module.Parse)
    #print(Parse.parse_sentence(parser_module.Parse,"donald"))
    search_engine.main()
    #file=open("Pickle_Save","rb")
    #db=pickle.load(file)
    #print(db)

    #file.close()
