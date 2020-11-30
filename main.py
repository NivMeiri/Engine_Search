import ast
import os
import re

from nltk.corpus import wordnet, stopwords

import search_engine

if __name__ == '__main__':
    # stop_words = stopwords.words('english')
    # print("IS" in stop_words)

    General_Posting = {"a": [1, {}], "b": [1, {}], "c": [1, {}], "d": [1, {}], "e": [1, {}], "f": [1, {}],
                            "g": [1, {}], "h": [1, {}], "i": [1, {}], "j": [1, {}], "k": [1, {}], "l": [1, {}],
                            "m": [1, {}], "n": [1, {}], "o": [1, {}], "p": [1, {}], "q": [1, {}], "r": [1, {}],
                            "s": [1, {}], "t": [1, {}], "u": [1, {}], "v": [1, {}], "w": [1, {}], "x": [1, {}],
                            "y": [1, {}], "z": [1, {}], "@": [1, {}], "#": [1, {}], "other": [1, {}]}

    corpus_path= 'C:/Users/Hadassa Zenou/Desktop/data'
    output_path="C:/Users/Hadassa Zenou/Documents/GitHub/Engine_Search"
    stemming=False
    queries=["Dr. Anthony Fauci wrote in a 2005 paper published in Virology Journal that hydroxychloroquine was effective in treating SARS."]
    num_docs_to_retrieve=20
    search_engine.main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve)

