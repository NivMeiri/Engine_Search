import ast
import pickle
import time
from math import log

from nltk.corpus import wordnet

from parser_module import Parse
from ranker import Ranker
import utils


class Searcher:

    def __init__(self, inverted_index,avg_doc,output,num_of_doc):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.ranker = Ranker()
        self.output=output
        self.inverted_index = inverted_index
        self.num_of_doc=num_of_doc
        self.avg_doc=avg_doc


    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """

        relevant_docs = {}
        temp_char = ""
        Word_net=[]
        for term in query:
            if term not in  self.inverted_index:
                Word_net+=self.WordNet(term)
            else:
                Word_net.append(term)
        expand_query = sorted(Word_net)
        print(expand_query)
        #searching the terms in posting files
        for term in expand_query:
             # an example of checks that you have to do
                if term in self.inverted_index:
                    idf = log(self.num_of_doc / self.inverted_index[term], 2)
                    if term[0]!=temp_char:
                        temp_char = term[0]
                        name=self.output+"/Pickles_directories"
                        if term[0]=="@":
                            name += "/@/final_dict_@.pkl"
                        elif term[0]=="#":
                            name += "/#/final_dict_#.pkl"
                        elif term[0].islower() or term[0].isupper():
                            name+="/"+term[0].lower()+"/final_dict_"+term[0].lower()+".pkl"
                        else:
                            name += "/other/final_dict_other.pkl"
                        db = open(name, 'rb')
                        posting = pickle.load(db)
                        db.close()
                    docs=posting[term]
                    for doc_tuple in docs:
                        doc = doc_tuple[0]
                        tf=doc_tuple[1]
                        len=doc_tuple[2]
                        bm25=self.ranker.rank_with_bm25(idf, tf, len, self.avg_doc)
                        if doc not in relevant_docs.keys():
                            relevant_docs[doc] = bm25
                        else:
                            relevant_docs[doc] += bm25

        return relevant_docs

    # if the word does not exist in the inverted we taking the two first synonyms
    def WordNet(self,word):
        word_counter=0
        synonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if(word_counter<2 and l.name not in synonyms):
                    synonyms.append(l.name())
                    word_counter+=1
        return(set(synonyms))