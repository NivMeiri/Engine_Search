import re

from nltk.corpus import wordnet

import search_engine

if __name__ == '__main__':
    corpus_path= 'C:/Users/Admin/Desktop/data/date=07-12-2020'
    output_path="C:/Users/Admin/Documents/GitHub/Engine_Search"
    stemming=False
    queries=["going"]
    num_docs_to_retrieve=20
    search_engine.main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve)
    #
    # word="good"
    # synonyms = []
    # for syn in wordnet.synsets(word):
    #     for l in syn.lemmas():
    #         synonyms.append(l.name())
    # print(set(synonyms))
    # print(len(set(synonyms)))
    #
    #

import json
data = {}
data['1'] = [1,2,3,{"aba":1,"saba":2,"sabta":3}]
data['2'] = [2,3,4,{"aaba":1,"asaba":2,"asabta":3}]
data['3'] = [3,4,5,{"baaba":1,"basaba":2,"basabta":3}]
with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)
