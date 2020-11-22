import pickle


class Indexer:
    def __init__(self, config):
        # the dictionary
        self.inverted_idx = {}
        #the posting files
        self.postingDict = {}
        # Dictionary for the docs... key= doc id... value={max tf, doc}
        self.doc_dictionary={}
        self.config = config
        self.saved_dict = {}
        # init the dictionaries by alpha bet probability
        self.A_dict={}
        self.B_C_D_dict={}
        self.E_dict={}
        self.F_G_H_dict={}
        self.I_dict={}
        self.J_K_l_M_dict={}
        self.N_dict={}
        self.O_dict={}
        self.P_Q_R_dict={}
        self.S_dict={}
        self.T_dict={}
        self.U_V_W_X_Y_Z_dict={}

    def add_new_doc(self, document):
        Indexer.num_of_doc = Indexer.num_of_doc + 1
        document_dictionary = document.term_doc_dictionary
        #adding the doc max term, doc term dictionary and the len of unique terms in the documenet
        self.doc_dictionary[document[0]]=(document.max_term,len(document_dictionary ),document_dictionary )
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
            self.add_to_Posting_sorted(toReturn,document.tweet_id,document_dictionary,term)
        if Indexer.num_of_doc==100000:
            self.save_with_pickle(self.postingDict)
        elif Indexer.num_of_doc%100000 == 0:
            self.merge_files()
                #print(self.postingDict)

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
    def add_to_Posting_sorted(self,toReturn,document_tweet_id,document_dictionary,term):
        my_list=self.postingDict[toReturn]
        for i in range (len(my_list)):
            if(my_list[i][0]>document_tweet_id):
                self.postingDict[toReturn].append((document_tweet_id, document_dictionary[term]))

    def merge_files_posting(self):
        saved_dict = self.load_dictionary()
        for term in self.postingDict:
            if term in saved_dict:
                for doc in self.postingDict[term]:
                    saved_dict[term].append(doc)
            else:
                saved_dict[term] = self.postingDict[term]
        self.save_with_pickle(saved_dict)
    def Add_toMatch_posting(self,letter):


