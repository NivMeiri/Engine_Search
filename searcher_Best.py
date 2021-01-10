
from math import log
from nltk.corpus import wordnet
from ranker import Ranker



#--------------this is the best search model------------------
class Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model
    # parameter allows you to pass in a precomputed model that is already in
    # memory for the searcher to use such as LSI, LDA, Word2vec models.
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None):
        self._parser = parser
        self._indexer = indexer
        self._ranker = Ranker()
        self._model = model
        self.entities=open("entities.txt").read().split()
        # DO NOT MODIFY THIS SIGNATURE
        # You can change the internal implementation as you see fit.

    def search(self, query, k):
        """
        Executes a query over an existing index and returns the number of
        relevant docs and an ordered list of search results (tweet ids).
        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relavant
            and the last is the least relevant result.
        """
        query_as_list = self._parser.parse_sentence(query)
        relevant_docs = self._relevant_docs_from_posting(query_as_list)
        n_relevant = len(relevant_docs)
        ranked_doc_ids = Ranker.rank_relevant_docs(relevant_docs)
        return n_relevant,ranked_doc_ids[:k]




    def _relevant_docs_from_posting(self, query_as_list):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: parsed query tokens
        :return: dictionary of relevant documents mapping doc_id to document frequency.
        """
        #     This function loads the posting list and count the amount of relevant documents per term.
        #     :param query: query
        #     :return: dictionary of relevant documents.
        #     """
        #
        avg_doc = self._indexer.avg_Size_doc / self._indexer.num_of_docs
        relevant_docs = {}
        temp_char = ""
        expand_query = sorted(self.WordNetExpand(query_as_list))

        for term in expand_query:
            term_lower = term.lower()
            if term in self._indexer.inverted_idx:
                idf = log(self._indexer.num_of_docs / self._indexer.inverted_idx[term_lower], 2)
                docs = self._indexer.postingDict[term_lower]
                for doc_tuple in docs:
                    doc = doc_tuple[0]
                    tf = doc_tuple[1]
                    len = doc_tuple[2]
                    bm25 = self._ranker.rank_with_bm25(idf, tf, len, avg_doc)
                    if(term.lower()  in self.entities or term.upper() in self.entities):
                        bm25=1.35*bm25
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


    def WordNetExpand(self,query):
        Word_net = []
        for term in query:
            if term not in self._indexer.inverted_idx:
                Word_net += self.WordNet(term)
            else:
                Word_net.append(term)
        return  Word_net

    def SpellChecker(self,word_list):
        after=[]
        print( "this is before spell checking :"+str(word_list) )
        spell = self.spell
        for value in word_list:
            after.append(spell.correction(value))
        print( "this is after spell checking :"+str(after) )
        return after
