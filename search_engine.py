import csv
import time
from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer_parta import Indexer
from searcher import Searcher
import utils

def run_engine(corpus_path,output_path,stemming):
    """
    # :return:
    # """
    if(stemming==True):
        output_path=output_path+"/WithStem"
    else:
        output_path=output_path+"/WithoutStem"
    num_of_docs = 0
    config = ConfigClass()
    p = Parse(stemming,output_path)
    indexer = Indexer(config,output_path)
    Files_directories = ["a","b", "c", "d","e", "f","g", "h", "i", "j", "k", "l","m", "n", "o", "p", "q", "r","s", "t", "u", "v", "w", "x","y", "z", "@", "#", "other"]
    r = ReadFile(corpus_path)
    documents_list = r.read_file_our_use(corpus_path)
    start=time.time()
    doc_id_counter=0
    num_of_Saving_doc=0
    #Iterate over every document in the directory -parsing and indexing
    for file in documents_list:
        file_open=r.read_Parquert(file)
        for idx, document in enumerate(file_open):
            parsed_document = p.parse_doc(document)
            num_of_docs += 1
            num_of_Saving_doc +=1
            indexer.add_new_doc(parsed_document)
            if (num_of_docs % 280000 == 0):
                num_of_Saving_doc = 0
                indexer.insert_posting()

    if( num_of_Saving_doc>0):
        indexer.insert_posting()
    p=""
    ##del p

    Entites_list=r.read_file_pickl(output_path + "/_Entities_pickles_")
    indexer.Check_Merge_entites(Entites_list)

    utils.save_obj(indexer.inverted_idx, "inverted_index")
    utils.save_obj(indexer.Doc_information, "Doc_info")
    indexer.Doc_information={}
    if(indexer.num_of_doc>0):
        avg=indexer.avg_doc/indexer.num_of_doc
    for director in Files_directories:
        documents_list = r.read_file_pickl(output_path + "/Pickles_directories"+"/"+director)
        indexer.Merge_into_28_pickles(documents_list,director)
    return [avg,indexer.Get_inverted(),num_of_docs]

def search_and_rank_query(query ,num_docs_to_retrieve,stemming,avg_doc,inverted_index,output,num_of_docs):
    p = Parse(stemming,output)
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index,avg_doc,output,num_of_docs)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, num_docs_to_retrieve)

def main(corpus_path,output_path,stemming,query_to_check,num_docs_to_retrieve):

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

    info_from_engine = run_engine(corpus_path, output_path, stemming)
    avg_doc = info_from_engine[0]
    inverted_index = info_from_engine[1]
    num_of_docs = info_from_engine[2]
    if (stemming):
        output_path = output_path + "/WithStem"
    else:
        output_path = output_path + "/WithoutStem"

    query_num =1
    for query in queries:
        start = time.time()
        for doc_tuple in search_and_rank_query(query ,num_docs_to_retrieve,stemming,avg_doc,inverted_index,output_path,num_of_docs):
            print('tweet id: {}, score (Rank with BM25 method): {}'.format(doc_tuple[0], doc_tuple[1]))
        query_num +=1


