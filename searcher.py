import ast

from nltk.corpus import wordnet

from parser_module import Parse
from ranker import Ranker
import utils


class Searcher:

    def __init__(self, inverted_index,doc_line):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.doc_line=doc_line
    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        #temp_query=[]
        #for word in query:
        #    temp_query+=(self.WordNet(word))
        #query+=temp_query
        posting = utils.load_obj("Pickle_Save_posting")
        relevant_docs = {}
        for term in query:
            try: # an example of checks that you have to do
                posting_doc = posting[term]
                for doc_tuple in posting_doc:
                    doc = doc_tuple[0]
                    if doc not in relevant_docs.keys():
                        doc_info=self.Load_Doc_Info(doc)
                        dict_info=doc_info[4]
                        sum_weight=0
                        for term_query in query:
                            if term_query in dict_info:
                                sum_weight+=dict_info[term_query][2]
                        cosim=self.ranker.Rank_with_cosimilarity(doc_info[2],len(query),sum_weight)
                        relevant_docs[doc] = cosim
            except:
                print('term {} not found in posting'.format(term))
        return relevant_docs


    def Load_Doc_Info (self,Doc_id):
            Doc_line = self.doc_line[Doc_id]
            fp = open("Documnet_info_Wij.txt")
            for i, line in enumerate(fp):
                if i+1 ==Doc_line:
                    line=ast.literal_eval(line)
                    line=line.decode( ("utf-8"))
                    line=ast.literal_eval(line)
                    fp.close()
                    return  line


    def WordNet(self,word):
        synonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        return(set(synonyms))
