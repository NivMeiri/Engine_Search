import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
from urllib.parse import urlparse

class Parse:
    def __init__(self):
        self.stop_words = stopwords.words('english')

    def parse_tags(self,term,text_tokensterm):
        hash_Tag = re.findall('[A-Z][^A-Z]*', term)
        for hash in hash_Tag:
            print(hash)
            text_tokensterm.append(hash)

    def parse_sentence(self, text):
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
            if x!=None and len(x)>0:
                # hashtag law
                if x[0] == "#":
                    text_tokensterm.append(list_of_words[i])
                    print(list_of_words[i])
                elif x[0] == "@":
                    text_tokensterm.append(list_of_words[i])
                    print(list_of_words[i])
                #URL law
                elif x[0] == "https":
                    UrlList=self.pars_url(list_of_words[i])
                    for word_in_url in UrlList:
                        text_tokensterm.append(word_in_url)
                        print(word_in_url)
                # number law-units and percent
                elif x[0].replace('.', '', 1).isdigit() or x[0].replace(',', '', 1).isdigit():
                    num = x[0]
                    if num.find(',') != -1:
                        newNum = num.split(",")
                        newNum2=''
                        for n in newNum:
                            newNum2 += n
                        num=newNum2
                    if i+1 < len(list_of_words):
                        if list_of_words[i+1] == "percent" or list_of_words[i+1] == "percentage" or list_of_words[i+1] == "Percent" or list_of_words[i+1] == "Percentage":
                            text_tokensterm.append(num+"%")
                            print(num+"%")
                        elif list_of_words[i+1] == "thousand":
                            text_tokensterm.append(num + "K")
                            print(num + "K")
                        elif list_of_words[i + 1] == "million":
                            text_tokensterm.append(num + "M")
                            print(num + "M")
                        elif list_of_words[i + 1] == "billion":
                            text_tokensterm.append(num + "B")
                            print(num + "B")
                        else:
                            num=self.to3digits_units(num)
                            text_tokensterm.append(num)
                            print(num)
                    else:
                        num=self.to3digits_units(num)
                        text_tokensterm.append(num)
                        print(num)
                else:
                    text_tokensterm.append(x[0])
                    print(x[0])


        # text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        return text_tokensterm


    def pars_url(self, url):
        import re
        l = re.split('[,|.|/|//|:%?=+]', url)
        a = []
        for x in l:
            if x is not '':
                a.append(x)
        print(a)
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
        print("---------------------------------------------------")
        print(num)
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

