import pickle


class Indexer:

    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config
        self.saved_dict={}

    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary.keys():
                upper = term.upper()
                lower = term.lower()
                toReturn=""
                # Update inverted index and posting
                if (lower not in self.inverted_idx):
                    # the word start with lower case char
                    if (term[0].islower() or (len(term)>1 and (term[0]=='@' or term[0]=='#') and term[1].islower())):
                        self.inverted_idx[lower] = 1
                        self.postingDict[lower]=[]
                        toReturn = lower
                        if (upper in self.inverted_idx):
                            self.inverted_idx[lower] += self.inverted_idx[upper]
                            self.inverted_idx.pop(upper, None)
                            self.postingDict[lower].append(self.postingDict[upper])
                            self.postingDict.pop(upper,None)

                    # the word start with upper case char
                    else:
                        toReturn = upper
                        if (upper in self.inverted_idx):
                            self.inverted_idx[upper] += 1
                        else:
                            self.inverted_idx[upper] = 1
                            self.postingDict[upper]=[]
                else:
                    self.inverted_idx[lower] += 1
                    toReturn=lower
                self.postingDict[toReturn].append((document.tweet_id, document_dictionary[term], len(document_dictionary)))
                #print(self.postingDict)

    def save_with_pickle(self,dict):
        db=open('Pickle_Save','ab')
        pickle.dump(dict, db)
        db.close()

    def load_dictionary(self):
        db=open('Pickle_Save','rb')
        dbfile=pickle.load(db)
        db.close()
        return  dbfile

    def merge_files(self):
        saved_dict = self.load_dictionary()
        for term in self.postingDict:
            if term in saved_dict:
                for doc in self.postingDict[term]:
                    saved_dict[term].append(doc)
            else:
                saved_dict[term] = self.postingDict[term]
        self.postingDict={}
        self.save_with_pickle(saved_dict)



