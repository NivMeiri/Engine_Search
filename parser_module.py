import re
from math import log
from nltk.corpus import wordnet
import nltk
from nltk.corpus import stopwords
from document import Document
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

class Parse:
    def __init__(self):
        self.stop_words = stopwords.words('english')
        words = open("word_freq.txt").read().split()
        self.wordcost = dict((k, log((i + 1) * log(len(words)))) for i, k in enumerate(words))
        self.maxword = max(len(x) for x in words)
        self.word_dict={}
    def parse_tags(self,term,text_tokensterm):
        if (term.isupper()):
            text_tokensterm.append(term)
        elif (term.islower()):
            hash_list = self.infer_spaces(term)
            for hash in hash_list:
                text_tokensterm.append(hash)
        else:
            hash_list = re.findall('[A-Z][^A-Z]*', term)
            for hash in hash_list:
                text_tokensterm.append(hash)

    def parse_sentence(self, text):
        self.Names_and_Entities(text)
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        text_tokensterm=[]
        #text_tokens = word_tokenize(text)
        ##todo clean the words after text re , . & |
        list_of_words=text.split(" ")
        last=''
        for i in range(0, len(list_of_words)):
            x=word_tokenize(list_of_words[i])

            if (x!=None and len(x)>0):
                # hashtag law
                if x[0] == "#" and  len(x)>1:
                    text_tokensterm.append(list_of_words[i])
                    self.parse_tags(x[1],text_tokensterm)
                elif x[0] == "@":
                    text_tokensterm.append(list_of_words[i])
                    #print(list_of_words[i])
                #URL law
                elif x[0] == "https":
                    UrlList=self.pars_url(list_of_words[i])
                    for word_in_url in UrlList:
                        text_tokensterm.append(word_in_url)
                        #print(word_in_url)
                # number law-units and percent
                elif self.to_number(x[0]).replace('.', '', 1).isdigit():
                    num = self.to_number(x[0])
                    if i+1 < len(list_of_words):
                        if list_of_words[i+1].lower() == "percent" or list_of_words[i+1].lower() == "percentage" :
                            text_tokensterm.append(num+"%")
                            #print(num+"%")
                        elif list_of_words[i+1].lower() == "thousand":
                            text_tokensterm.append(num + "K")
                            #print(num + "K")
                        elif list_of_words[i + 1].lower() == "million":
                            text_tokensterm.append(num + "M")
                            #print(num + "M")
                        elif list_of_words[i + 1].lower() == "billion":
                            text_tokensterm.append(num + "B")
                            #print(num + "B")
                        else:
                            num=self.to3digits_units(num)
                            text_tokensterm.append(num)
                            #print(num)
                    else:
                        num=self.to3digits_units(num)
                        text_tokensterm.append(num)
                        #print(num)
                else:
                    self.Upper_Lowe_Case_Words(x[0])
                    text_tokensterm.append(x[0])

        text_tokens_without_stopwords = [w.lower() for w in text_tokensterm if w not in self.stop_words]
        return text_tokens_without_stopwords


    def pars_url(self, url):
        import re
        l = re.split('[,|/|//|:%?=+]', url)
        a = []
        for x in l:
            if x is not '':
                a.append(x)
        return a
    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = self.pars_url(doc_as_list[3])
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)

        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        #print("full text:  "+full_text)
        #print(term_dict.keys())
        return document

    def to3digits_units(self, num):
        num_to_units = float(num)
        if (num_to_units >= 1000) and (num_to_units < 1000000):
            num_to_units = num_to_units/1000
            return self.round3(str(num_to_units))+"K"
        elif (num_to_units >= 1000000) and (num_to_units < 1000000000):
            num_to_units = num_to_units / 1000000
            return self.round3(str(num_to_units)) + "M"
        elif num_to_units >= 1000000000:
            num_to_units = num_to_units / 1000000000
            return self.round3(str(num_to_units)) + "B"
        else:
            return self.round3(str(num_to_units))

    def round3(self, num):
        newNum = round(float(num), 3)
        num_with_point = str(newNum).split(".")
        while len(num_with_point[1])>0 and num_with_point[1][-1]=='0':
            num_with_point[1]=num_with_point[1][:-1]
        if len(num_with_point[1])==0:
            return str(num_with_point[0])
        else:
            return str(num_with_point[0])+'.'+str(num_with_point[1])

    def Upper_Lowe_Case_Words(self,word):

        upper=word.upper()
        lower=word.lower()
        #checking that the word isnt empty string
        if(len(word)>0 and word!=None):
            if(lower not in self.word_dict):
                #the word start with lower case char
                if(word[0].islower()):
                    self.word_dict[lower] = 1
                    if(upper in self.word_dict):
                        self.word_dict[lower]+=self.word_dict[upper]
                        self.word_dict.pop(upper, None)
                # the word start with upper case char
                else:
                    if(upper in self.word_dict):
                        self.word_dict[upper]+=1
                    else:
                        self.word_dict[upper]=1
            else:
                self.word_dict[lower]+=1



    def  Names_and_Entities(self, text):
        tokens = word_tokenize(text)
        pos=(nltk.pos_tag(tokens))
        my_NE_word=nltk.ne_chunk(pos)

    def infer_spaces(self,s):
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


    def get_continuous_chunks(self,text):
        '''
        chunked = ne_chunk(pos_tag(word_tokenize(text)))
        continuous_chunk = []
        current_chunk = []
        for i in chunked:
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            if current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                current_chunk = []
            else:
                         continue
        if (continuous_chunk in self.word_dict):
            self.word_dict[continuous_chunk] += 1
        else:
            self.word_dict[continuous_chunk] = 1'''

    def to_number(self,num):
        newNum = num.split(",")
        newNum2 = ''
        for n in newNum:
            newNum2 += n
        return newNum2

