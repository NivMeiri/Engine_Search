import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
from urllib.parse import urlparse

class Parse:
    #word_to_sepearate_url={'/':1,"//":1,":":1,";":1,".":1,"?":1,"=":1}
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
        print("##############")
        print(text)
        ##todo clean the words after text re , . & |
        list_of_words=text.split(" ")
        for term in list_of_words:
            x=word_tokenize(term)
            if(x!=None and len(x)>0):
                if (term[0] == "#"):
                    text_tokensterm.append(term)
                    print(term)
                elif (term[0] == "@"):
                    text_tokensterm.append(term)
                    print(term)
                elif x[0]=="https":
                    UrlList=self.pars_url(term)
                    for word_in_url in UrlList:
                        text_tokensterm.append(word_in_url)
                        print(word_in_url)
                else:
                    text_tokensterm.append(x[0])
                    print(x[0])

        # text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        # return text_tokens_without_stopwords
    def pars_url(self,url):
        list=url.split('/')
        return list
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
