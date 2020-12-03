import math
from math import  log,sqrt
from nltk.corpus import wordnet

class Ranker:
    def __init__(self):
        pass
    @staticmethod
    def rank_relevant_doc(relevant_doc):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param relevant_doc: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        return sorted(relevant_doc.items(), key=lambda item: item[1], reverse=True)

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=2000):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """

        return sorted_relevant_doc[:k]
    # N is the number of docs in the corpus
    # n_qi , the number of docs that contain the term

    #W_iq is the number of times that the term exist in the query


    def Rank_with_cosimilarity(self, relevant_doc,query):
        wiq=len(query)
        for doc in relevant_doc.keys():
            sum=(relevant_doc[doc][1]/(math.sqrt(relevant_doc[doc][0]*wiq)))
            relevant_doc[doc]=sum
        return  (relevant_doc)
    # calculating the rank with the bm25 formula
    def rank_with_bm25(self,idf,tf,d,avg):
        k = 1.2
        b = 0.75
        bm25 = (idf * tf * (k + 1)) / (tf + k*(1 - b + b * (d / avg)))
        return bm25
