import os.path
from math import log
from nltk.corpus import stopwords
import re
from document import Document
import stemmer
import utils


class Parse:
    def __init__(self,is_stemming,output_path):
        self.output=output_path+"/"+"_Entities_pickles_"
        self.stop_words = stopwords.words('english')
        # helper functions for the hashtag calculation
        self.words = open("word_freq.txt").read().split()
        self.wordcost = dict((k, log((i + 1) * log(len(self.words)))) for i, k in enumerate(self.words))
        self.maxword = max(len(x) for x in self.words)

        # dict for the terms that suspected of being entities
        self.entities = {}
        self.Counter_entites = 1

        #Binary parameter from main that decide if the parser use stemming
        self.binary_Stem = is_stemming
        if(is_stemming):
            self.stemmer = stemmer.Stemmer().Porter_stemmer

        # Months dictionary to support our new rule,saving all dates in the same format
        self.month = {"jan": "01", "january": "01", "feb": "02", "february": "02", "mar": "03", "march": "03",
                      "apr": "04", "april": "04", "may": "05", "jun": "06", "june": "06", "jul": "07", "july": "07",
                      "aug": "08", "august": "08", "sep": "09", "september": "09", "october": "10", "oct": "10",
                      "nov": "11", "november": "11", "dec": "12", "december": "12"}

        # making dir for the entities pickles
        path=self.output
        if not os.path.isdir(path):
            os.mkdir(self.output)

    #the main function of this class,parsing the full text from the read files
    def parse_sentence(self, text):
        #saving the entities
        if(len(self.entities)>200000):
            utils.save_obj(self.entities, self.output +"/"+ str(self.Counter_entites)+ "_entities_")
            self.Counter_entites+=1
            self.entities={}

        text_tokenstream = []
        list_of_words =text.split()
        # running over the terms in the full text and clean them from unnecessary chars and emojis
        for i in range(0, len(list_of_words)):
            term = self.clean(list_of_words[i])

            #remove stop words, "RT", empty strings from the text.
            if len(term)>0 and term.lower() not in self.stop_words and term.upper() != "RT":
                    if term[0] == "#":
                        text_tokenstream.append(term)

                        #Hash tag rule,explained in the function
                        self.parse_tags(term[1:], text_tokenstream)

                     # saving tags with the @ sign
                    elif term[0] == "@":
                        text_tokenstream.append(term)

                     #if the term end with % add the term
                    elif term[-1] in "%":
                        text_tokenstream.append(term)

                    # url rule, pars it and save the url terms
                    elif term[0:5] == "https":
                        UrlList = self.pars_url(term[5:])
                        for word_in_url in UrlList:
                            self.clean(word_in_url)
                            text_tokenstream.append(word_in_url.lower())

                    #if term is month sent it to date function
                    elif term.lower() in self.month:
                        self.to_date(term.lower(), list_of_words, i, text_tokenstream)

                    #check if the term is number and remove it ", ." and then implementing the Numbers rule
                    elif re.sub('[,]', '',term).replace('.', '', 1).isdigit() and term.isascii():
                        num = re.sub('[,]', '',term)
                        if i + 1 < len(list_of_words):
                            if list_of_words[i + 1].lower() == "percent" or list_of_words[i + 1].lower() == "percentage":
                                text_tokenstream.append(self.to3digits_units(num) + "%")
                                list_of_words[i + 1] = ""
                            elif list_of_words[i + 1].lower() == "thousand":
                                text_tokenstream.append(num + "K")
                                list_of_words[i + 1] = ""
                            elif list_of_words[i + 1].lower() == "million":
                                text_tokenstream.append(num + "M")
                                list_of_words[i + 1] = ""
                            elif list_of_words[i + 1].lower() == "billion":
                                text_tokenstream.append(num + "B")
                                list_of_words[i + 1] = ""
                            else:
                                if "/" in list_of_words[i + 1] and list_of_words[i + 1].replace('/', '', 1).isdigit():
                                    num = self.to3digits_units(num)+" "+list_of_words[i+1]
                                    list_of_words[i+1] = ""
                                else:
                                    num = self.to3digits_units(num)
                                text_tokenstream.append(num)
                        else:
                            num = self.to3digits_units(num)
                            text_tokenstream.append(num)
                    else:
                        if term.lower()=="covid-19" or term.lower()=="covid19" or term.lower()=="covid_19" or term.lower()=="cov19" or term.lower()=="cov-19" or term.lower()=="covid":
                            text_tokenstream.append("COVID19")
                        # if the terms not fit any rule, removing the unnecessary chars
                        list_term = re.split('[-,|/|//|:.%?=+]', term)
                        for word in list_term:
                            self.clean_and_push(word , text_tokenstream)

        # send the parsed text to the entities func
        self.Entites_and_Names(text_tokenstream)
        return text_tokenstream

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text =doc_as_list[2]
        url = doc_as_list[3]
        retweet_text =doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)
        doc_length = len(tokenized_text)  # after text operations.
        max_term = ("", 0)
        index = 0
        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = (1, [index])
            else:
                term_dict[term][1].append(index)
                term_dict[term] = (term_dict[term][0] + 1, term_dict[term][1])
            if term_dict[term][0] > max_term[1]:
                max_term = (term, term_dict[term][0])
            index+=1

        # we decided to add two more important fields:  max term in tweet  and len of the tweet after parsed(not unique)
        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length, max_term, len(tokenized_text))
        return document


    '''hash tag function- we support in these rules: 1. seperate by Upper case... e.g #DonaldTrump
    2. sepearate by _ sign e.g #donald_trump 3. seperate by rate function e.g #donaldtrump
    '''
    def parse_tags(self, term, text_tokensterm):
        hash_list = []
        if term.islower():
            # apply the third rule
            hash_list = self.infer_spaces(term)
        elif "_" in term:
            hash_list = term.split("_")
        elif term.isupper() == False:
            hash_list = re.findall('[A-Z][^A-Z]*', term)
        for hash in hash_list:
            self.clean_and_push(hash, text_tokensterm)
        if term not in hash_list:
            self.clean_and_push(term, text_tokensterm)


    def infer_spaces(self, s):
        """Uses dynamic programming to infer the location of spaces in a string
        without spaces."""

        # Find the best match for the i first characters, assuming cost has
        # been built for the i-1 first characters.
        # Returns a pair (match_cost, match_length).
        def best_match(i):
            candidates = enumerate(reversed(cost[max(0, i - self.maxword):i]))
            return min((c + self.wordcost.get(s[i - k - 1:i], 9e999), k + 1) for k, c in candidates)
        # Build the cost array.
        cost = [0]
        for i in range(1, len(s) + 1):
            c, k = best_match(i)
            cost.append(c)
        # Backtrack to recover the minimal-cost string.
        out = []
        i = len(s)
        while i > 0:
            c, k = best_match(i)
            assert c == cost[i]
            out.append(s[i - k:i])
            i -= k
        return out

    #clean the term from unncessary chars and emojis
    def clean(self, term):
        while len(term) > 0:
            if term[-1] in '/(.&…),''`;:-_|!?"' or term[-1] in "'" or ord(term[-1]) > 126:
                term = term[:-1]
            elif term[0] in '/()&.…,''`;:-_|!?"' or term[0] in "'" or ord(term[0]) > 126:
                term = term[:0]
            else:
                break
        return term

    # if the parser include stemming it will happen here, because thats the place the terms that not belonge to any other rule arriving
    def clean_and_push(self, term, text_tokensterm):
        term=self.clean(term)
        if len(term) > 0:
            if term[0].isupper():
                term = term.upper()
            else:
                term = term.lower()
            if self.binary_Stem:
                term = self.stemmer.stem(term)
            else:
                term = self.end_with_s(term)
            text_tokensterm.append(term)

    # another rule that we added ( arent we amazing?)- LOL, remove the "'s" in the word
    def end_with_s(self,term):
        if term.lower().endswith("'s"):
            return term[:-2]
        else:
            return term

    def pars_url(self, url):
        l = re.split('[,|/|//|:%?=+]', url)
        a = []
        for x in l:
            if x is not '':
                a.append(x)
        return a
    #this funtion get a term that suspected to be a part of a date and return it as a date in our single format
    def to_date(self,term,list_of_words,i,text_tokensterm):
        date = ""
        if i>0 and list_of_words[i-1].isdigit() and len(list_of_words[i-1]) < 3:
            date = list_of_words[i-1]+"-"+self.month.get(term)
            text_tokensterm.pop()
        elif i>0 and list_of_words[i-1].isdigit() and len(list_of_words[i-1]) <= 4:
            date = self.month.get(term)+"-"+list_of_words[i - 1]
            text_tokensterm.pop()
        elif i>0 and (list_of_words[i-1].endswith("st") or list_of_words[i-1].endswith("th")) and list_of_words[i-1][0:-2].isdigit():
            date = list_of_words[i - 1][:-2] + "-" + self.month.get(term)
            text_tokensterm.pop()
        if i+1<len(list_of_words):
            clean_num=self.clean(list_of_words[i+1])
            if clean_num.isdigit() and len(clean_num)<3:
                date = clean_num + "-" + self.month.get(term)
                list_of_words[i + 1]=""
            elif clean_num.isdigit() and len(list_of_words[i+1]) <= 4:
                if len(date)>0:
                    date = date+"-" + clean_num
                else:
                    date = self.month.get(term)+"-"+clean_num
                list_of_words[i + 1] = ""
            elif (clean_num.endswith("st") or clean_num.endswith("th")) and clean_num[0:-2].isdigit():
                date = clean_num[:-2] + "-" + self.month.get(term)
                list_of_words[i + 1] = ""
        if len(date)==0:
            date = term
        text_tokensterm.append(date)

    # this function get number and return it like required in Numbers rule(1000=1k,1000000=1m... )
    def to3digits_units(self, num):
        num_to_units = float(num)
        if (num_to_units >= 1000) and (num_to_units < 1000000):
            num_to_units = num_to_units / 1000
            return self.round3(str(num_to_units)) + "K"
        elif (num_to_units >= 1000000) and (num_to_units < 1000000000):
            num_to_units = num_to_units / 1000000
            return self.round3(str(num_to_units)) + "M"
        elif num_to_units >= 1000000000:
            num_to_units = num_to_units / 1000000000
            return self.round3(str(num_to_units)) + "B"
        else:
            return self.round3(str(num_to_units))
    #round to 3 digits after the dot
    def round3(self, num):
        newNum = round(float(num), 3)
        num_with_point = str(newNum).split(".")
        while len(num_with_point[1]) > 0 and num_with_point[1][-1] == '0':
            num_with_point[1] = num_with_point[1][:-1]
        if len(num_with_point[1]) == 0:
            return str(num_with_point[0])
        else:
            return str(num_with_point[0]) + '.' + str(num_with_point[1])
    #this function maintain a entities dictionary like the rules demand
    def Entites_and_Names(self,list_of_words):
        length=len(list_of_words)
        for i in range(len(list_of_words)) :
            Tag_Names = re.findall("\A@", list_of_words[i])
            if (len(Tag_Names) > 0):
                self.check_if_in_entites_dictionary(list_of_words[i][1:].upper())
            elif(list_of_words[i][0].isupper):
                if(length>i+1 and len(list_of_words[i+1])>0):
                    if(list_of_words[i+1][0].isupper()):
                        my_String=list_of_words[i].upper()+" "+list_of_words[i+1].upper()
                        self.check_if_in_entites_dictionary(my_String)
                else:
                    self.check_if_in_entites_dictionary(list_of_words[i].upper())

    def check_if_in_entites_dictionary(self,entite):
        if( entite in self.entities):
            self.entities[entite]+=1
        else:
            self.entities[entite]=1



