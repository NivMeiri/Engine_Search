# DO NOT MODIFY CLASS NAME
import pickle
import utils

class Indexer:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config
        self.avg_Size_doc=0
        self.num_of_docs=0
        self.doc_info={}

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        self.num_of_docs+=1

        document_dictionary = document.term_doc_dictionary
        self.avg_Size_doc+=document.doc_length
        # Go over each term in the doc
        for term in document_dictionary.keys():
            term_lower=term.lower()
            try:
                # Update inverted index and posting
                if term_lower not in self.inverted_idx.keys():
                    self.inverted_idx[term_lower] = 1
                    self.postingDict[term_lower] = []
                else:
                    self.inverted_idx[term_lower] += 1
                freq=document.term_doc_dictionary[term][0]/(document.max_term[1])
                self.postingDict[term_lower].append((document.tweet_id,freq,document.doc_length))


            except Exception:
                print(Exception)
                print('problem with the following key {}'.format(term[0]))

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        db = open(fn, 'rb')
        dbfile = pickle.load(db)
        db.close()
        return dbfile
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        utils.save_obj(fn,"inverted_idx")

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _is_term_exist(self, term):
        """
        Checks if a term exist in the dictionary.
        """
        return term in self.postingDict

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def get_term_posting_list(self, term):
        """
        Return the posting list from the index for a term.
        """
        return self.postingDict[term] if self._is_term_exist(term) else []

    def add_square_Wij(self):
        for term in self.inverted_idx:
            idf=self.inverted_idx[term]
            list_of_doc=self.postingDict[term]
            for doc in list_of_doc:
                if doc[0] in self.doc_info:
                    self.doc_info[doc[0]][0]+=1
                    self.doc_info[doc[0]][1] += (idf*doc[1])**2
                else:
                    tf_idf=(idf*doc[1])**2
                    self.doc_info[doc[0]]=[1,tf_idf]