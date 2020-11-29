import ast
import linecache
import math
import pickle
from math import log
import os.path

import utils


class Indexer:
    num_of_doc=0
    def __init__(self, config,output_path):
        self.inverted_idx = {}
        self.General_Posting={"a":[1,{}],"b":[1,{}],"c":[1,{}],"d":[1,{}],"e":[1,{}],"f":[1,{}],"g":[1,{}],"h":[1,{}],"i":[1,{}],"j":[1,{}],"k":[1,{}],"l":[1,{}],"m":[1,{}],"n":[1,{}],"o":[1,{}],"p":[1,{}],"q":[1,{}],"r":[1,{}],"s":[1,{}],"t":[1,{}],"u":[1,{}],"v":[1,{}],"w":[1,{}],"x":[1,{}],"y":[1,{}],"z":[1,{}],"@":[1,{}],"#":[1,{}],"other":[1,{}]}
        self.TO_posting_info_a= {}
        self.Doc_information={}
        self.config = config
        self.output_path=output_path + "/Pickles_directories"

        os.mkdir(self.output_path)
        for key in self.General_Posting.keys():
            os.mkdir(self.output_path + "/" + key)

    def add_new_doc(self, document):
        Indexer.num_of_doc = Indexer.num_of_doc + 1
        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        #the upper lower sort.. decide if the word will be saved in upper or lower case and update the matches terms
        for term in document_dictionary.keys():
            upper = term.upper()
            lower = term.lower()
            toReturn=upper
            if (term[0].islower()or ((term[0] == '@' or term[0] == '#') and (len(term) > 1)  and term[1].islower())):
                toReturn = lower
            # Update inverted index and posting
            upper_in_posting=upper in self.inverted_idx
            lower_in_posting=lower in self.inverted_idx
            term_already_exist=upper_in_posting or lower_in_posting
            #new word to the corpus
            if(not(term_already_exist)):
                    self.inverted_idx[toReturn] = 1
            elif(lower_in_posting ):
                    self.inverted_idx[lower]+= 1
                    toReturn=lower
                #switch from upper in inverted to lower. all the words will be saved in lower
            #upper in posting.. we need to switch them if the term is lower,else just add it to exist value
            else:
                if (toReturn==lower):
                    self.inverted_idx[lower]=self.inverted_idx[upper]+1
                    self.inverted_idx.pop(upper, None)
                    # switch from upper in inverted to lower. all the words will be saved in lower
                else:
                    toReturn=upper
                    self.inverted_idx[upper] +=  1
            freq=document.term_doc_dictionary[term][0]/(document.max_term[1])
            first_term=toReturn[0].lower()
            #"a": [0, {}]
            if(first_term not in self.General_Posting ):
                if toReturn in self.General_Posting["other"][1]:
                    self.General_Posting["other"][1][toReturn].append([document.tweet_id, freq])
                else:
                    self.General_Posting["other"][1][toReturn] = [[document.tweet_id, freq]]
                # if (len(self.General_Posting["other"][1]) == 25000):
                #     self.insert_to_post( "other")
            else:
                if toReturn in self.General_Posting[first_term]:
                    self.General_Posting[first_term][1][toReturn].append([document.tweet_id,freq])
                else:
                    self.General_Posting[first_term][1][toReturn]=[[document.tweet_id,freq]]
                # if(len(self.General_Posting[first_term][1])==25000):
                #     self.insert_to_post(first_term)
        self.Doc_information[document.tweet_id]=document.len_doc

    #self.doc_info(document)
        #if Indexer.num_of_doc%100000==0:
            #self.save_with_pickle()
            #self.save_file_Info()

    def load_dictionary(self,name):
        db=open(name,'rb')
        dbfile=pickle.load(db)
        db.close()
        return  dbfile

    def merge_and_save_posting(self):
        saved_dict = self.load_dictionary()
        for term in self.postingDict:
            if term in saved_dict:
                for doc in self.postingDict[term]:
                    saved_dict[term].append(doc)
            else:
                saved_dict[term] = self.postingDict[term]
        self.postingDict=saved_dict
        self.save_with_pickle()

    def insert_posting(self):
        for key in self.General_Posting.keys():
            name = self.output_path+"/"+key+"/"+'Pickl_posting' + str(key)+"_ "+str(self.General_Posting[key][0])+ ".pkl"
            self.General_Posting[key][0]+=1
            db = open(name, "wb")
            pickle.dump(self.General_Posting[key][1], db)
            db.close()
            self.General_Posting[key][1] = {}


    def Merge_into_28_pickles(self,documents_list, char):
        if(len(documents_list)>0):
            our_dict=self.load_dictionary(documents_list[0])
        for i in range (1,len( documents_list)):
            temp_dict=utils.load_obj(documents_list[i])
            for term in temp_dict:
                    if term in our_dict:
                        our_dict[term] += temp_dict[term]
                    else:
                        our_dict[term] = temp_dict[term]
        utils.save_obj(our_dict,self.output_path+"/"+char+"/"+"final_dict"+char )
        # os.remove(documents_list[i])
