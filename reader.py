import os
import pandas as pd


class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def read_file(self, file_name):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        full_path = os.path.join(self.corpus_path, file_name)
        tweet=[]
        i=0
        path_list=[full_path]
        if not full_path.endswith(".parquet"):
            while len(path_list)>0:
                for subdir, dirs, files in os.walk(path_list.pop(0)):
                    for filename in files:
                        filepath=subdir+os.sep+filename
                        if filepath.endswith("parquet"):
                            df = pd.read_parquet(filepath, engine="pyarrow").values.tolist()
                            for doc in df:
                                tweet.append(doc)
                    for dirname in dirs:
                        path_list.append(subdir+os.sep+dirname)


        else:
            tweet=pd.read_parquet(full_path, engine="pyarrow").values.tolist()
        return tweet
