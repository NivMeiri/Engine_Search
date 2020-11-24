import ast
import linecache
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

    # define list of places

    # dict=[1,2,3,4]
    # with open('listfile.txt', 'w') as filehandle:
    #     for i in range (100):
    #         filehandle.write('%s\n' % (dict))
    # x=linecache.getline("listfile.txt", 100, module_globals=None)
    #
    #
    # x=ast.literal_eval(x)
    # print(type(x))
    # print(x)

    search_engine.main()
    #file=open("Pickle_Save","rb")
    #db=pickle.load(file)
    #print(db)
    # line = ast.literal_eval("[('#covidã¼19', 1), 14, {'#covidã¼19': (1, [0]), 'covidã¼19': (1, [1]), 'claim': (1, [2]), 'life': (1, [3]), '@wsbradio': (1, [4]), 'host': (1, [5]), '@thehermancain': (1, [6]), '#coverageyoucancounton': (1, [7]), 'coverag': (1, [8]), 'you': (1, [9]), 'can': (1, [10]), 'count': (1, [11]), 'On': (1, [12]), 'coverageyoucancounton': (1, [13])}]")
    # print(line)
    # print(type(line))
    # for i in line:
    #     print(i)

    #file.close()
