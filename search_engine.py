import time
from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
import pandas as pd


def run_engine(corpus_path,output_path,stemming):
    """
    :return:
    """
    num = 0
    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse(stemming)
    indexer = Indexer(config)
   # indexer.save_with_pickle({})
#todo get the file name
    start=time.time()
    documents_list = r.read_file(corpus_path)
    #documents_list = r.read_file(file_name='sample3.parquet')
    # Iterate over every document in the file
    for file in documents_list:
        documents_list=read_Parquert(file)
        for idx, document in enumerate(documents_list):
            parsed_document = p.parse_doc(document)
            num += 1
            indexer.add_new_doc(parsed_document)
        print("num of tweets:  " + str(num) )
        print("time that  pars+indexing:  "+ str(file)+":  "+ str(time.time() - start))
    indexer.merge_all_posting()
    print("the posting dict was merged and saved:  " + str(file) + ":  " + str(time.time() - start))
        # index the document data
    indexer.add_wij_to_doc()
    print("time that  calc wij:  " + str(file) + ":  " + str(time.time() - start))

    # delete the entities that occur less then twice
    #indexer(parser.entities_dict)

    print('Finished parsing and indexing. Starting to export files')
    print("time that toke to pars:  "+str(time.time()-start))
    #todo check what to do with the indexer and posting that they saved
    utils.save_obj(indexer.inverted_idx, "inverted_idx")
    utils.save_obj(indexer.Doc_Line_Number, "Doc_Line_Number")

def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    Doc_line=utils.load_obj("Doc_Line_Number")
    return (inverted_index,Doc_line)

def search_and_rank_query(query, inverted_index,doc_line ,k,stem):
    p = Parse(stem)
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index,doc_line,stem)
    print("start search")
    start=time.time()
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    print(time.time()-start)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)

def main(corpus_path,output_path,stemming,queries,num_docs_to_retrieve):
    start=time.time()
    run_engine(corpus_path,output_path,stemming)
    #info=load_index()
    # inverted_index = info[0]
    # Doc_line=info[1]
    # for query in queries:
    #     for doc_tuple in search_and_rank_query(query, inverted_index,Doc_line, num_docs_to_retrieve,stemming):
    #         print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
    # print("total time:    "+str(time.time()-start))

def main2():
    run_engine()
    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    info=load_index()
    inverted_index = info[0]
    Doc_line=info[1]
    for doc_tuple in search_and_rank_query(query, inverted_index,Doc_line, k):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))


def read_Parquert(filepath):
    tweets=[]
    df = pd.read_parquet(filepath, engine="pyarrow").values.tolist()
    for doc in df:
        tweets.append(doc)
    return tweets