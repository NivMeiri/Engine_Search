import ast
import pickle
import time
from math import log

from nltk.corpus import wordnet

from parser_module import Parse
from ranker import Ranker
import utils


class Searcher:

    def __init__(self, inverted_index,doc_line,avg_doc,stem,output):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse(stem,output)
        self.ranker = Ranker()
        self.output=output
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
        # expand_query=[]
        # for term in query:
        #     expand_query+=self.WordNet(term)
        temp_char = ""
        Word_net=[]
        for term in query:
            if term not in  self.inverted_index:
                # print('term {} not found in posting'.format(term))
                # print("Searching the word in the WordNet model")
                Word_net+=self.WordNet(term)
            else:
                Word_net.append(term)
        expand_query = sorted(Word_net)
        print(expand_query)
        for term in expand_query:
             # an example of checks that you have to do
                if term in self.inverted_index:
                    idf = log(self.num_of_doc / self.inverted_index[term], 2)
                    if term[0]!=temp_char:
                        temp_char = term[0]
                        name=self.output+"/Pickles_directories"
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
        word_counter=0
        synonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if(word_counter<2 and l.name not in synonyms):
                    synonyms.append(l.name())
                    word_counter+=1
        return(set(synonyms))
