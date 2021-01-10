import time

import pandas as pd
from parser_module import Parse
from indexer_Spacy import Indexer
from searcher_Spacy import Searcher
import utils
import pickle
# DO NOT CHANGE THE CLASS NAME
#------------------------------------this moudle is implementing Spacy Entities Search Engine-------------------------------
class SearchEngine:

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation, but you must have a parser and an indexer.
    def __init__(self, config=None):
        self._config = config
        self._parser = Parse()
        self._indexer = Indexer(config)
        self._model =  None

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

        def is_ascii(s):
            return all(ord(c) < 128 for c in s)

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

        #this funtion is respobsible to write the entities dict to text file


        #def write_entites():
        # file1 = open("entities.txt", "a")
        # start=time.time()
        # our_dict = sorted(self._parser.entities.items(), key=lambda item: item[1], reverse=True)
        # print(our_dict)
        # for word in our_dict:
        #     if is_ascii(word[0]):
        #         parsed=self._parser.parse_sentence(word[0])
        #         for term in parsed:
        #             if(not   term[0].isdigit() and   term[0]!="#" and term[0]!="@"):
        #                 file1.writelines(str(term)+"\n")
        # file1.close()


        to_del=[]

        # saving the necessary data to pickle
        to_Save = (self._indexer.inverted_idx, self._indexer.postingDict, self._indexer.num_of_docs, self._indexer.avg_Size_doc)
        utils.save_obj(to_Save, "index_5")


        def remove_word_1():
            for key in self._indexer.inverted_idx:
                if (self._indexer.inverted_idx[key] == 1 and key.isalpha()==False):
                    to_del.append(key)
                    self._indexer.postingDict.pop(key)
            for key in to_del:
                self._indexer.inverted_idx.pop(key)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        obj=utils.load_obj(fn)
        self._indexer.inverted_idx=obj[0]
        self._indexer.postingDict=obj[1]
        self._indexer.num_of_docs=obj[2]
        self._indexer.avg_Size_doc=obj[3]
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



