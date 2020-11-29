import ast
import linecache
import math
import pickle
from math import log
import os.path


class Indexer:
    num_of_doc=0
    def __init__(self, config):
        # the Main Dictionary {Term:unique doc,line in posting}
        self.inverted_idx = {}
        #the posting files   {term: [(doc1,freq in doc),(doc3,8),(doc5,7)]-sorted list by doc id}
        #alpha_bet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        #             "u", "v", "w", "x", "y", "z", "@", "#", "other"]
        # for word in alpha_bet:
        #     name = "Posting_files" + word + ".txt"
         #   open(name, 'a')
        # dictionary to retreive the line number of specific key..{doc id:line number in text file}
        self.Doc_Line_Number = {}
        # [doc id,[doc info]]....doc info=[max_term(str),max freq(int),unique terms(int),wij^2,dictionary{term:(freq,indices(list),wij}
        self.Doc_Info_Text = []
        #counter for the line in the text to write
        self.Next_line = 1
        self.Posting_counter=1
        self.my_files=[]
        #self.General_Posting={"a":[1,{}],"b":[1,{}],"c":[1,{}],"d":[1,{}],"e":[1,{}],"f":[1,{}],"g":[1,{}],"h":[1,{}],"i":[1,{}],"j":[1,{}],"k":[1,{}],"l":[1,{}],"m":[1,{}],"n":[1,{}],"o":[1,{}],"p":[1,{}],"q":[1,{}],"r":[1,{}],"s":[1,{}],"t":[1,{}],"u":[1,{}],"v":[1,{}],"w":[1,{}],"x":[1,{}],"y":[1,{}],"z":[1,{}],"@":[1,{}],"#":[1,{}],"other":[1,{}]}
        self.TO_posting_info_a= {}
        self.config = config



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
                    self.inverted_idx[toReturn] = [1,None]
            elif(lower_in_posting ):
                    self.inverted_idx[lower] [0]+=1
                    toReturn=lower
                #switch from upper in inverted to lower. all the words will be saved in lower
            #upper in posting.. we need to switch them if the term is lower,else just add it to exist value
            else:
                if (toReturn==lower):
                    self.inverted_idx[lower]=[self.inverted_idx[upper][0]+1,self.inverted_idx[upper][1]]
                    self.inverted_idx.pop(upper, None)
                    # switch from upper in inverted to lower. all the words will be saved in lower
                else:
                    toReturn=upper
                    self.inverted_idx[upper][0] +=  1

            freq=document.term_doc_dictionary[term][0]/(document.max_term[1])
            first_term=toReturn[0].lower()
            #"a": [0, {}]
            if(first_term not in self.General_Posting ):
                if toReturn in self.General_Posting["other"][1]:
                    self.General_Posting["other"][1][toReturn].append([document.tweet_id, freq])
                else:
                    self.General_Posting["other"][1][toReturn] = [[document.tweet_id, freq]]
                if (len(self.General_Posting["other"][1]) == 12000):
                    self.insert_to_post( "other")
            else:
                if toReturn in self.General_Posting[first_term]:
                    self.General_Posting[first_term][1][toReturn].append([document.tweet_id,freq])
                else:
                    self.General_Posting[first_term][1][toReturn]=[[document.tweet_id,freq]]
                if(len(self.General_Posting[first_term][1])==12000):
                    self.insert_to_post(first_term)


        # if ( len(self.TO_posting_info)%150000==0):
        #     self.insert_to_post( )
        self.doc_info(document)
        if Indexer.num_of_doc%100000==0:
            #self.save_with_pickle()
            self.save_file_Info()





    def add_new_doc2(self, document):
        #print(document.full_text)
        Indexer.num_of_doc = Indexer.num_of_doc + 1
        document_dictionary = document.term_doc_dictionary
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        # Go over each term in the doc
        #the upper lower sort.. decide if the word will be saved in upper or lower case and update the matches terms
        for term in document_dictionary.keys():
            upper = term.upper()
            lower = term.lower()
            toReturn=""
            # Update inverted index and posting
            if (lower not in self.inverted_idx):
                # the word start with lower case char
                if (term[0].islower()) or (len(term)>1 and term[1].islower() and (term[0]=='@' or term[0]=='#')):
                    self.inverted_idx[lower] = 1
                    self.postingDict[lower]=[]
                    toReturn = lower
                    if (upper in self.inverted_idx):
                        self.inverted_idx[lower] += self.inverted_idx[upper]
                        self.inverted_idx.pop(upper, None)
                        if upper in self.postingDict:
                            self.postingDict[lower] += self.postingDict[upper]
                            self.postingDict.pop(upper, None)
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

            self.add_to_Posting_sorted(toReturn,document.tweet_id,document.term_doc_dictionary[term][0]/(document.max_term[1]))
        self.doc_info(document)
        if Indexer.num_of_doc%250000==0:
            self.save_with_pickle()
            self.save_file_Info()


            #self.Load_Doc_Info(document.tweet_id)


    def save_with_pickle(self):
        name='Pickl_posting'+str(self.Posting_counter)+".pkl"
        self.Posting_counter+=1
        self.my_files.append(name)
        db=open(name,"wb")
        pickle.dump(self.postingDict, db)
        db.close()
        self.postingDict = {}

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

    def save_file_Info(self):
        #check if the file is already exist
        if(os.path.isfile("Documnet_info.txt")):
            param="a"
        else:
            param="w"
        with open('Documnet_info.txt', param) as my_file:
                for doc in self.Doc_Info_Text:
                    my_string=str(doc[1])
                    if my_string.isascii():
                        my_file.write('%s\n' % (my_string))
                    self.Doc_Line_Number[doc[0]]=self.Next_line
                    self.Next_line+=1
        self.Doc_Info_Text=[]

    def Load_Doc_Info (self,Doc_id):
        Doc_line = self.Doc_Line_Number[Doc_id]
        fp = open("Documnet_info_Wij.txt")
        for i, line in enumerate(fp):
            if i ==Doc_line:
                #x=linecache.getline("listfile.txt", Doc_line, module_globals=None)
                line=ast.literal_eval(line)
                return  line
        #fp.close()
        #x = linecache.getline("Documnet_info.txt", Doc_line, module_globals=('UTF-8'))
        #x=ast.literal_eval(x)
        #return  x

    def add_to_Posting_sorted(self, toReturn, document_tweet_id, frequency):
        if((self.postingDict[toReturn]==[])):
            self.postingDict[toReturn].append((document_tweet_id,frequency))
        else:
            #index = self.binary_insert(self.postingDict[toReturn], document_tweet_id)
            self.postingDict[toReturn].insert(0, (document_tweet_id, frequency))

    def binary_insert(self, list_doc, doc_id):
        low = 0
        high = len(list_doc) - 1
        mid = 0
        doc_id=str(doc_id)
        while low < high:
            mid = (low + high) // 2
            if doc_id < list_doc[mid][0]:
                high = mid
            else:
                low = mid + 1
        return low

    def doc_info(self, doc):
        text_info = [doc.max_term[0],doc.max_term[1], len(doc.term_doc_dictionary),doc.term_doc_dictionary]
        self.Doc_Info_Text.append((doc.tweet_id, text_info))

    def insert_to_post(self,char):
            dictionary=self.General_Posting[char][1]
            #check if the file is already exist
            with open("Posting_files"+char+".txt", 'a') as my_file:
                for key in dictionary.keys():
                    to_insert = str(dictionary[key])
                    if(key in self.inverted_idx):
                        if self.inverted_idx[key][1]==None:
                            my_file.write('%s\n' % (to_insert))
                        else:
                            old=self.read_specific_line("Posting_files"+char+".txt",self.inverted_idx[key] [1])
                            old=""
                            to_add=old+to_insert
                            my_file.write('%s\n' % (to_add))

                        self.inverted_idx[key][1] = self.General_Posting[char][0]
                        self.General_Posting[char][0] += 1
                self.General_Posting[char][1]={}


    def read_specific_line(self,filename,line_num):
            with open(filename, 'r') as my_file:
                for i, line in enumerate(my_file):
                    if i+1 == line_num:
                        return line






        # else:
        #     #read the current line and write to it
        #     with open('posting_files.txt', 'r') as my_file:
        #         for i, line in enumerate(my_file):
        #             if (i == self.inverted_idx[to_ret][1]):
        #                 line = line+my_string
        #                 with open('posting_files.txt', 'w') as my_file:
        #                     if line.isascii():
        #                         my_file.write('%s\n' % (line))
        #                     self.Posting_files_line += 1


    def add_wij_to_doc(self):
        counter=0
        list_of_docs=[]
        with open('Documnet_info.txt', 'r') as to_read:
            for i, line in enumerate(to_read):
                line = ast.literal_eval(line)
                list_of_docs.append( line)
                counter+=1
                if(counter==10000):
                    self.writing_wij_to_text(list_of_docs)
                    counter=0
                    list_of_docs=[]

    def writing_wij_to_text(self,list_of_docs):
        square_wij = 0
        with open('Documnet_info_Wij.txt', 'w') as to_write:
            for doc_info_list in list_of_docs:
                doc_term = doc_info_list[3]
                for term in doc_term:
                    temp_term = term.lower()
                    if (temp_term not in self.inverted_idx):
                        temp_term = term.upper()
                    wij = self.calc_wij(doc_term[term][0], doc_info_list[1], self.inverted_idx[temp_term], self.num_of_doc)
                    square_wij += (wij ** 2)
                doc_info_list[3] = doc_term
                doc_info_list.insert(3, square_wij)
                new_info = [doc_info_list[1], doc_info_list[2], doc_info_list[3]]
                to_write.write('%s\n' % (str(new_info)))

    def calc_wij(self, fi,max_fi, df, n):
        return (fi/max_fi) * (log(n/df, 2))

    def merge_all_posting(self):
        for file in (self.my_files):
            saved_dict=self.load_dictionary(file)
            for term in saved_dict:
                if term in self.postingDict:
                    self.postingDict[term]+=saved_dict[term]
                else:
                    self.postingDict[term] = saved_dict[term]
        self.save_with_pickle()