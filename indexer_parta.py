import pickle
import os.path
import utils

class Indexer_part_A:
    num_of_doc=0
    #TODO REMOVE OUTPUT_PATH FROM INPUT
    def __init__(self, config):
        self.inverted_idx = {}
        # create the main dictionary for postings.  explained in the report
        self.General_Posting={"a":[1,{}],"b":[1,{}],"c":[1,{}],"d":[1,{}],"e":[1,{}],"f":[1,{}],"g":[1,{}],"h":[1,{}],"i":[1,{}],"j":[1,{}],"k":[1,{}],"l":[1,{}],"m":[1,{}],"n":[1,{}],"o":[1,{}],"p":[1,{}],"q":[1,{}],"r":[1,{}],"s":[1,{}],"t":[1,{}],"u":[1,{}],"v":[1,{}],"w":[1,{}],"x":[1,{}],"y":[1,{}],"z":[1,{}],"@":[1,{}],"#":[1,{}],"other":[1,{}]}
        self.Doc_information={}
        self.config = config
        #self.output_path=output_path + "/Pickles_directories"
        self.avg_doc=0
        #os.mkdir(self.output_path)
        #create a dir to each term
        # for key in self.General_Posting.keys():
        #     os.mkdir(self.output_path + "/" + key)

    def Get_inverted(self):
        return  self.inverted_idx

    def Get_Doc(self):
        return self.Doc_information

    #the main function of this class, getting doc from parser and indexing it
    def add_new_doc(self, document):
        Indexer.num_of_doc = Indexer.num_of_doc + 1
        document_dictionary = document.term_doc_dictionary
        self.avg_doc+=document.len_doc

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
                    self.inverted_idx[toReturn] =1
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
                    self.inverted_idx[upper] +=1


            freq=document.term_doc_dictionary[term][0]/(document.max_term[1])
            first_term=toReturn[0].lower()

            #adding to term to the match dictionary by its first letter
            if(first_term not in self.General_Posting ):
                if toReturn in self.General_Posting["other"][1]:
                    self.General_Posting["other"][1][toReturn].append((document.tweet_id, freq,document.len_doc))
                else:
                    self.General_Posting["other"][1][toReturn] = [(document.tweet_id, freq,document.len_doc)]

            else:
                if toReturn in self.General_Posting[first_term][1]:
                    self.General_Posting[first_term][1][toReturn].append((document.tweet_id,freq,document.len_doc))
                else:
                    self.General_Posting[first_term][1][toReturn]=[(document.tweet_id,freq,document.len_doc)]

        self.Doc_information[document.tweet_id]=[document.len_doc, len(document.term_doc_dictionary), document.max_term[1]]



    def load_dictionary(self,name):
        db=open(name,'rb')
        dbfile=pickle.load(db)
        db.close()
        return  dbfile
    # saving the posting files in the directories
    def insert_posting(self):
        for key in self.General_Posting.keys():
            name = self.output_path+"/"+key+"/"+'Pickl_posting_' + str(key)+str(self.General_Posting[key][0])+ ".pkl"
            self.General_Posting[key][0]+=1
            db = open(name, "wb")
            pickle.dump(self.General_Posting[key][1], db)
            db.close()
            self.General_Posting[key][1] = {}
    # this func will execute once the indexer finish his job,creating main 29 posting files [a,b,c.....z,other,#,@]
    def Merge_into_28_pickles(self,documents_list, char):
        if(len(documents_list)>0):
            our_dict = self.load_dictionary(documents_list[0])
            os.remove(documents_list[0])
            for i in range (1,len( documents_list)):
                temp_dict=self.load_dictionary(documents_list[i])
                for term in temp_dict:
                        if term in our_dict:
                            our_dict[term] += temp_dict[term]
                        else:
                            our_dict[term] = temp_dict[term]
                os.remove(documents_list[i])
            self.General_Posting[char]={}
            utils.save_obj(our_dict,self.output_path+"/"+char+"/"+"final_dict_"+char )
    #check if the entities found more then once , if not remove it from the inverted files
    def Check_Merge_entites(self,entities):
        our_dict={}
        for i in range (len( entities)):
            temp_dict=self.load_dictionary(entities[i])
            for term in temp_dict:
                    if term in our_dict:
                        our_dict[term] += temp_dict[term]
                    else:
                        our_dict[term] = temp_dict[term]
            os.remove(entities[i])
        for key in our_dict.keys():
            if our_dict[key]<2:
                if(key in self.inverted_idx):
                    self.inverted_idx.pop(key)
    #TODO implement this method
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        raise NotImplementedError

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        raise NotImplementedError

    # feel free to change the signature and/or implementation of this function
    # or drop altogether.
    def _is_term_exist(self, term):
        """
        Checks if a term exist in the dictionary.
        """
        return term in self.postingDict

    # feel free to change the signature and/or implementation of this function
    # or drop altogether.
    def get_term_posting_list(self, term):
        """
        Return the posting list from the index for a term.
        """
        return self.postingDict[term] if self._is_term_exist(term) else []
