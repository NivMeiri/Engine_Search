import ast
import pickle
import time
from math import log

from nltk.corpus import wordnet

from parser_module import Parse
from ranker import Ranker
import utils


class Searcher:

    def __init__(self, inverted_index,doc_line,avg_doc,stem):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse(stem)
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.doc_line=doc_line
        self.num_of_doc=len(self.doc_line)
        self.avg_doc=avg_doc

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """

        relevant_docs = {}
        for term in query:
             # an example of checks that you have to do
                if term in self.inverted_index:
                    idf = log(self.num_of_doc/self.inverted_index[term], 2)
                    name='C:/Users/Hadassa Zenou/Documents/GitHub/Engine_Search/Pickles_directories'
                    if term[0]=="@":
                        name += "/@/final_dict@.pkl"
                    elif term[0]=="#":
                        name += "/#/final_dict#.pkl"
                    elif term[0].islower() or term[0].isupper():
                        name+="/"+term[0].lower()+"/final_dict"+term[0].lower()+".pkl"
                    else:
                        name += "/other/final_dictother.pkl"
                    db = open(name, 'rb')
                    posting = pickle.load(db)
                    db.close()
                    docs=posting[term]
                    for doc_tuple in docs:
                        doc = doc_tuple[0]
                        tf=doc_tuple[1]
                        bm25=self.ranker.rank_with_bm25(idf,tf,self.doc_line[doc],self.avg_doc)
                        if doc not in relevant_docs.keys():
                            relevant_docs[doc]=bm25
                        else:
                            relevant_docs[doc]+=bm25
                else:
                    print('term {} not found in posting'.format(term))
        return relevant_docs


    def Load_Doc_Info (self,Doc_id):
            Doc_line = self.doc_line[Doc_id]
            fp = open("Documnet_info_Wij.txt")
            for i, line in enumerate(fp):
                if i+1 ==Doc_line:
                    line = ast.literal_eval(line)
                    line = line.decode( ("utf-8"))
                    line = ast.literal_eval(line)
                    fp.close()
                    return line


    def WordNet(self,word):
        synonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        return(set(synonyms))