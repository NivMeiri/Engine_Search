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
        # tranforming to panda.
        tweets = []
        i = 0
        if not full_path.endswith(".parquet"):
            for subdir, dirs, files in os.walk(full_path):
                for filename in files:
                    filepath = subdir + os.sep + filename
                    if filepath.endswith(".parquet"):
                        df = pd.read_parquet(filepath, engine="pyarrow").values.tolist()
                        for doc in df:
                            tweets.append(doc)

        else:
            tweets = pd.read_parquet(full_path, engine="pyarrow").values.tolist()
        return tweets
