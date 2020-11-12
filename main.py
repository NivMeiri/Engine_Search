import search_engine
import numpy
import pandas as pd
from reader import ReadFile
import nltk
if __name__ == '__main__':
    print( numpy.__version__)
    #df = pd.read_parquet("C:\Users\Admin\Desktop\Data\date=08-07-2020\covid19_08-07.snappy.parquet", engine="pyarrow")
    #print(df[0])
    #r = ReadFile("C:/Users/Admin/Desktop/Data/date=07-20-2020")
    #print(len(r))
    #readfile = r.read_file("covid19_07-20.snappy.parquet")

    # for n in readfile:
    #     num = 0
    #     for l in n:
    #         num+=1
    #         if l!=None:
    #             print(str(num)+") "+l)
    print("COVID-19".isupper())
    search_engine.main()

    from math import log

    # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).


