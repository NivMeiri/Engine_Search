import time
from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils

def run_engine(corpus_path,output_path,stemming):
    """
    :return:
    """
    num = 0
    config = ConfigClass()
    p = Parse(stemming,output_path)
    indexer = Indexer(config,output_path)
    Files_directories = ["a","b", "c", "d","e", "f","g", "h", "i", "j", "k", "l","m", "n", "o", "p", "q", "r","s", "t", "u", "v", "w", "x","y", "z", "@", "#", "other"]
    r = ReadFile(corpus_path)
    start=time.time()
    documents_list = r.read_file_our_use(corpus_path)
    # Iterate over every document in the file
    for file in documents_list:
        documents_list=r.read_Parquert(file)
        for idx, document in enumerate(documents_list):
            parsed_document = p.parse_doc(document)
            num += 1
            indexer.add_new_doc(parsed_document)
            if (num % 300000 == 0):
                indexer.insert_posting()
        print("num of tweets:  " + str(num) )
        print("time that  pars+indexing:  "+ str(file)+":  "+ str(time.time() - start))

    for director in Files_directories:
        documents_list = r.read_file_pickl(output_path + "/Pickles_directories"+"/"+director)
        Entites_list=r.read_file_pickl(output_path + "/_Entities_pickles_"+"/"+director)
        indexer.Merge_into_28_pickles(documents_list,director)
        indexer.Check_Merge_entites(Entites_list)
    if(indexer.num_of_doc>0):
        avg=indexer.avg_doc/indexer.num_of_doc
    utils.save_obj(indexer.inverted_idx,"inverted_index")
    utils.save_obj(indexer.Doc_information,"Doc_info")
    print("time that toke to pars+index+merge:  "+str(time.time()-start))
    return [avg,indexer.Get_Doc(),indexer.Get_inverted()]

def search_and_rank_query(query ,num_docs_to_retrieve,stemming,avg_doc,Doc_line,inverted_index,output):
    p = Parse(stemming,output)
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index,Doc_line,avg_doc,stemming,output)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, num_docs_to_retrieve)

def main(corpus_path,output_path,stemming,queries,num_docs_to_retrieve):
    info_from_engine=run_engine(corpus_path,output_path,stemming)
    avg_doc=info_from_engine[0]
    Doc_info=info_from_engine[1]
    inverted_index=info_from_engine[2]
    for query in queries:
        start = time.time()
        for doc_tuple in search_and_rank_query(query ,num_docs_to_retrieve,stemming,avg_doc,Doc_info,inverted_index,output_path):
            print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
        print("total time:    "+str(time.time()-start))
