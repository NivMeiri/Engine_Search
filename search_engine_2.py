import time

#---------------this moudle advanced parser--------------
import pandas as pd
from reader import ReadFile
from configuration import ConfigClass
from parser_module_Advance import Parse
from indexer import Indexer
from searcher import Searcher
import utils
import pickle

# DO NOT CHANGE THE CLASS NAME
class SearchEngine:

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation, but you must have a parser and an indexer.
    def __init__(self, config=None):
        self._config = config
        self._parser = Parse()
        self._indexer = Indexer(config)
        self._model = None

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def build_index_from_parquet(self, fn):
        """
        Reads parquet file and passes it to the parser, then indexer.
        Input:
            fn - path to parquet file
        Output:
            No output, just modifies the internal _indexer object.
        """
        df = pd.read_parquet(fn, engine="pyarrow")
        documents_list = df.values.tolist()
        # Iterate over every document in the file
        number_of_documents = 0
        for idx, document in enumerate(documents_list):
            # parse the document
            parsed_document = self._parser.parse_doc(document)
            number_of_documents += 1
            # index the document data
            self._indexer.add_new_doc(parsed_document)

        to_del=[]
        print("total num of terms: "+str(len(self._indexer.inverted_idx)))
        def remove_word_1():
            for key in self._indexer.inverted_idx:
                if (self._indexer.inverted_idx[key] == 1 and key.isalpha()==False):
                    to_del.append(key)
                    self._indexer.postingDict.pop(key)
            for key in to_del:
                self._indexer.inverted_idx.pop(key)

        remove_word_1()
        self._indexer.add_square_Wij()
        print("num of terms without the term with freq 1: " + str(len(self._indexer.inverted_idx)))
        utils.save_obj(self._indexer.postingDict,"posting")
        utils.save_obj(self._indexer.inverted_idx, "inverted_idx")
        print('Finished parsing and indexing.')
        #(sorted( self._indexer.inverted_idx,key=lambda x: self._indexer.inverted_idx[x]))
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        with open(fn ,'rb') as f:
            return pickle.load(f)


    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_precomputed_model(self,model_dir=None):
        """
        Loads a pre-computed model (or models) so we can answer queries.
        This is where you would load models like word2vec, LSI, LDA, etc. and
        assign to self._model, which is passed on to the searcher at query time.
        """
        pass

        # DO NOT MODIFY THIS SIGNATURE
        # You can change the internal implementation as you see fit.

    def search(self, query,k=2000):
        """
        Executes a query over an existing index and returns the number of
        relevant docs and an ordered list of search results.
        Input:
            query - string.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relavant
            and the last is the least relevant result.
        """
        searcher = Searcher(self._parser, self._indexer)
        return searcher.search(query,k)



    def main(self,output_path,stemming,query_to_check,num_docs_to_retrieve):
        self.build_index_from_parquet("data/benchmark_data_train.snappy.parquet")
        if isinstance(query_to_check, list):
            queries = query_to_check
        elif isinstance(query_to_check, str):
            if query_to_check.endswith(".txt"):
                try:
                    with open(query_to_check, "r",encoding="utf-8") as queries:
                        queries = queries.readlines()
                        query2 = []
                        for q in queries:
                            if (q != "\n"):
                                query2.append(q)
                        queries=query2
                except FileNotFoundError as e:
                    print(e)
            else:
                queries = [query_to_check]
        else:
            return

        if (stemming):
            output_path = output_path + "/WithStem"
        else:
            output_path = output_path + "/WithoutStem"

        query_num =1
        for query in queries:
            start = time.time()
            mylist=self.search(query, num_docs_to_retrieve)
            answer_to_run=mylist[1]
            for doc_tuple in answer_to_run:
                print('tweet id: {}'.format(doc_tuple))
            query_num += 1
            print("time that toke to retrieve :" + str(time.time() - start))



