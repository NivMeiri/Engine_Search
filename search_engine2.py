import time

import pandas as pd

from parser_module_SpellCorrection import Parse
from indexer import Indexer
from searcher import Searcher
import utils
#-----------------this model is implementing spellcorrection-----------------------------


# DO NOT CHANGE THE CLASS NAME
class SearchEngine:

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation, but you must have a parser and an indexer.
    def __init__(self, config=None):
        self._config = config
        self._parser = Parse()
        self._indexer = Indexer(config)
        self._model ="SpellCorrection"

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
        start=time.time()
        # Iterate over every document in the file
        number_of_documents = 0
        for idx, document in enumerate(documents_list):
            # parse the document
            parsed_document = self._parser.parse_doc(document)
            number_of_documents += 1
            # index the document data
            self._indexer.add_new_doc(parsed_document)
        print("after parsing and indexing :"+str(time.time()-start))
        utils.save_obj(self._indexer.inverted_idx, "inverted_idx")
        utils.save_obj(self._indexer.postingDict, "posting")
        print('Finished parsing and indexing.')

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        self._indexer.load_index(fn)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_precomputed_model(self):
        """
        Loads a pre-computed model (or models) so we can answer queries.
        This is where you would load models like word2vec, LSI, LDA, etc. and
        assign to self._model, which is passed on to the searcher at query time.
        """
        pass

        # DO NOT MODIFY THIS SIGNATURE
        # You can change the internal implementation as you see fit.

    def search(self, query, k=2000):
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
        searcher = Searcher(self._parser, self._indexer,self._model)
        return searcher.search(query, k)

    def main(self, output_path, stemming, query_to_check, num_docs_to_retrieve):
        self.build_index_from_parquet("data/benchmark_data_train.snappy.parquet")
        if isinstance(query_to_check, list):
            queries = query_to_check
        elif isinstance(query_to_check, str):
            if query_to_check.endswith(".txt"):
                try:
                    with open(query_to_check, "r", encoding="utf-8") as queries:
                        queries = queries.readlines()
                        query2 = []
                        for q in queries:
                            if (q != "\n"):
                                query2.append(q)
                        queries = query2
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

        query_num = 1
        for query in queries:
            start = time.time()
            for doc_tuple in self.search(query, num_docs_to_retrieve):
                print('tweet id: {}, score (Rank with BM25 method): {}'.format(doc_tuple[0], doc_tuple[1]))
            query_num += 1
            print("time that toke to retrieve :" + str(time.time() - start))


