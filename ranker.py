from math import  log,sqrt

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
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """

        return sorted_relevant_doc[:k]
    # N is the number of docs in the corpus
    # n_qi , the number of docs that contain the term
    def Idf_Rank(self,N,n_qi):
        return log((N-n_qi+0.5)/n_qi+0.5)
    #W_iq is the number of times that the term exist in the query
    def Rank_with_cosimilarity(self,Idf,tf,W_iq):
        return  (W_iq*tf*Idf)/sqrt((W_iq**2)*((tf*Idf)**2))