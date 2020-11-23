import ast
import linecache
import pickle
class Indexer:
    num_of_doc=0
    def __init__(self, config):
        # the dictionary
        self.inverted_idx = {}
        #the posting files
        self.postingDict = {}
        # Dictionary for the docs... key= doc id... value={max tf, doc}
        self.doc_dictionary={}
        self.config = config
        self.saved_dict = {}
        self.Doc_Line_Number={}
        self.Next_line=1
        self.Doc_Info_Text=[]
        # init the dictionaries by alpha bet probability


    def add_new_doc(self, document):
        Indexer.num_of_doc = Indexer.num_of_doc + 1
        document_dictionary = document.term_doc_dictionary
        #adding the doc max term, doc term dictionary and the len of unique terms in the documenet
        #self.doc_dictionary[document[0]]=(document.max_term,len(document_dictionary ),document_dictionary )
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        # Go over each term in the doc
        for term in document_dictionary.keys():
            upper = term.upper()
            lower = term.lower()
            toReturn=""
            # Update inverted index and posting
            if (lower not in self.inverted_idx):
                # the word start with lower case char
                if ( term[0].islower()) or (len(term)>1 and term[1].islower() and (term[0]=='@' or term[0]=='#') ):
                    self.inverted_idx[lower] = 1
                    self.postingDict[lower]=[]
                    toReturn = lower
                    if (upper in self.inverted_idx):
                        self.inverted_idx[lower] += self.inverted_idx[upper]
                        self.inverted_idx.pop(upper, None)
                        if upper in self.postingDict:
                            self.postingDict[lower].append(self.postingDict[upper])
                            self.postingDict.pop(upper,None)

                # the word start with upper case char
                else:
                    toReturn = upper
                    if (upper in self.inverted_idx):
                        self.inverted_idx[upper] += 1
                        if upper not in self.postingDict:
                            self.postingDict[upper] = []
                    else:
                        self.inverted_idx[upper] = 1
                        self.postingDict[upper]=[]
            else:
                self.inverted_idx[lower] += 1
                if lower not in self.postingDict:
                    self.postingDict[lower] = []
                toReturn=lower
        self.postingDict[toReturn].append((document.tweet_id,document_dictionary[term]))
        self.doc_info(document)
        if Indexer.num_of_doc==5:
            self.save_with_pickle()
            self.save_file_Info()
        elif Indexer.num_of_doc%2 == 0:
            self.merge_files_posting()
            self.save_file_Info()
            #print("this is the load"+str(self.Load_Doc_Info(document.tweet_id)))

    def save_with_pickle(self):
        db=open('Pickle_Save_posting',"wb")
        pickle.dump(self.postingDict, db)
        db.close()
        self.postingDict = {}

    def load_dictionary(self):
        db=open('Pickle_Save_posting','rb')
        dbfile=pickle.load(db)
        db.close()
        return  dbfile

    #self.add_to_Posting_sorted(toReturn, document.tweet_id, document_dictionary[term])

    def add_to_Posting_sorted(self,toReturn,document_tweet_id,freqency):
        index=0
        self.postingDict[toReturn].insert(index,(document_tweet_id, freqency))

    def merge_files_posting(self):
        saved_dict = self.load_dictionary()
        for term in self.postingDict:
            if term in saved_dict:
                for doc in self.postingDict[term]:
                    saved_dict[term].append(doc)
            else:
                saved_dict[term] = self.postingDict[term]
        self.postingDict=saved_dict
        self.save_with_pickle()

    #self.Doc_Info_Text=[(doc_id,[(max_term,term),unique_Terms,dict])]

    def save_file_Info(self):
        import os.path
        #check if the file is already exist
        if(os.path.isfile("Documnet_info.txt")):
            param="a"
        else:
            param="w"
        with open('Documnet_info.txt', param) as my_file:
                for doc in self.Doc_Info_Text:
                    print(doc[1])
                    my_file.write('%s\n' % (str(doc[1])))
                    self.Doc_Line_Number[doc[0]]=self.Next_line
                    self.Next_line+=1
        self.Doc_Info_Text=[]

    def Load_Doc_Info (self,Doc_id):
        Doc_line=self.Doc_Line_Number[Doc_id]
        x = linecache.getline("Documnet_info.txt",1, module_globals=None)
        x = ast.literal_eval(x)
        return  x

    def add_to_Posting_sorted(self, toReturn, document_tweet_id, frequency):
        index = self.binary_insert(self.postingDict[toReturn], document_tweet_id)
        self.postingDict[toReturn].insert(index, (document_tweet_id, frequency))

    def binary_insert(self, list_doc, doc_id):
        low = 0
        high = len(list_doc) - 1
        mid = 0
        while low <= high:
            mid = (high + low) // 2
            if (mid == low) and (doc_id < list_doc[high][0]) and (doc_id > list_doc[low][0]):
                return high

            elif list_doc[mid][0] < doc_id:
                low = mid + 1

            elif list_doc[mid][0] > doc_id:
                high = mid - 1

    def doc_info(self, doc):
        text_info = [doc.max_term, len(doc.term_doc_dictionary), doc.term_doc_dictionary]
        self.Doc_Info_Text.append((doc.tweet_id, text_info))