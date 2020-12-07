# Search_Engine
This is the general instruction for executing our project

We will explain about every class and how to use it.

1.main class- in the main class we will execute the search_engine.main() method,
Method signature: search_engine.main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve)
 
parameters that’s need to be sended by the user:
corpus path: the full path of the data that build the engine
output path: the full path to the dirs that posting will be write in
stemming: binary pararm.
Queries: list of quries strings or path to a text file.
num_docs_to_retrieve -as the name saying

2. Search engine class - this class is actually in charge of the entire engine and the integration between its parts.
Important Methods: run_engine, search and rank,main
The first method "run_engine" responsibility is to execute the reader, parser and indexer together and actually to build the corpus ,build the data to be used in the retrieval .
The search and rank method is responsible to return a list of related  docs to the query.
The main function is responsible to excute run engine and then to each quert call for the search_and_rank_query and return the match answers.

3.reader class
This class's purpose is to read the data from the parquet files, moreover we added methods that support read from posting picklfiles and also return list with the names in the directory

4. parser_module class
Getting the data from reader and parse each document, send it to the indexer

5.indexer class
Building the inverted index, the doc info dictionary and the main part- posting files.

6. ranker class
Responsible for ranking the docs and the queries with BM25 method

7.stemmer class
Simple class- have an instance of porterStemmer inside it

8.document
Define the structure of regular document from the data.
The files that we be saving while running the project:
In the outputpath we are assuming that there is two empty dir, WithStem and WithoutStem, after the running there will be in the match files according to stemming parameter two directories, "_Entities_pickles_" 1 for entites and the other  " Pickles_directories" for posting files, there will be 29 directorites, one to each char, other, # and @. In the project directory there will be two files: inverted_index and doc_info.
