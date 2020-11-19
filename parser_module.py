import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
import re
from math import log

class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')
        words = open("word_freq.txt").read().split()
        self.wordcost = dict((k, log((i + 1) * log(len(words)))) for i, k in enumerate(words))
        self.maxword = max(len(x) for x in words)
        self.word_dict = {}
        self.month = {"jan": "01", "january": "01", "feb": "02", "february": "02", "mar": "03", "march": "03",
                      "apr": "04", "april": "04", "may": "05", "jun": "06", "june": "06", "jul": "07", "july": "07",
                      "aug": "08", "august": "08", "sep": "09", "september": "09", "october": "10", "oct": "10",
                      "nov": "11", "november": "11", "dec": "12", "december": "12"}


    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        #self.Names_and_Entities(text)
        text_tokensterm = []
        ##todo clean the words after text re , . & |
        list_of_words = text.split()

        list_of_words = [w.lower() for w in list_of_words if w not in self.stop_words]
        for i in range(0, len(list_of_words)):
            term = self.clean(list_of_words[i])
            if len(term) > 0:
                ###hash tag law
                if term[0] == "#":
                    text_tokensterm.append(term)
                    self.parse_tags(term[1:], text_tokensterm)
                elif term[0] == "@":
                    text_tokensterm.append(term)
                elif term[-1] in "%":
                    text_tokensterm.append(term)
                elif term[0:5] == "https":
                    UrlList = self.pars_url(term)
                    for word_in_url in UrlList:
                        self.clean_and_push(word_in_url,text_tokensterm)
                elif term.lower() in self.month:
                    self.to_date(term.lower(), list_of_words, i, text_tokensterm)
                elif self.to_number(term).replace('.', '', 1).isdigit() and term.isascii():
                    num = self.to_number(term)
                    if i + 1 < len(list_of_words):
                        if list_of_words[i + 1].lower() == "percent" or list_of_words[i + 1].lower() == "percentage":
                            text_tokensterm.append(self.to3digits_units(num) + "%")
                            list_of_words[i + 1] = ""
                        elif list_of_words[i + 1].lower() == "thousand":
                            text_tokensterm.append(num + "K")
                            list_of_words[i + 1] = ""
                        elif list_of_words[i + 1].lower() == "million":
                            text_tokensterm.append(num + "M")
                            list_of_words[i + 1] = ""
                        elif list_of_words[i + 1].lower() == "billion":
                            text_tokensterm.append(num + "B")
                            list_of_words[i + 1] = ""
                        else:
                            num = self.to3digits_units(num)
                            text_tokensterm.append(num)
                    else:
                        num = self.to3digits_units(num)
                        text_tokensterm.append(num)
                else:
                    text_tokensterm.append(term)
        return text_tokensterm

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        #print(full_text)
        tokenized_text = self.parse_sentence(full_text)
        #print(tokenized_text)
        doc_length = len(tokenized_text)  # after text operations.

        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document


    def parse_tags(self, term, text_tokensterm):
        if (term.isupper()):
            self.clean_and_push(term,text_tokensterm)
        elif (term.islower()):
            hash_list = self.infer_spaces(term)
            for hash in hash_list:
                self.clean_and_push(hash,text_tokensterm)
        else:
            hash_list = re.findall('[A-Z][^A-Z]*', term)
            for hash in hash_list:
                self.clean_and_push(hash,text_tokensterm)


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

    def clean_and_push(self, term, text_tokensterm):
        term= self.clean(term)
        if len(term) > 0:
            text_tokensterm.append(term)

    def clean(self, term):
        while len(term) > 0:
            if term[-1] in '/(.&…),''`;:-|!?"' or term[-1] in "'" or ord(term[-1]) > 126:
                term = term[:-1]
            elif term[0] in '/()&.…,''`;:-|!?"' or term[0] in "'" or ord(term[0]) > 126:
                term = term[:0]
            else:
                break
        return term

    def pars_url(self, url):
        l = re.split('[,|/|//|:%?=+]', url)
        a = []
        for x in l:
            if x is not '':
                a.append(x)
        return a

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

    def round3(self, num):
        newNum = round(float(num), 3)
        num_with_point = str(newNum).split(".")
        while len(num_with_point[1]) > 0 and num_with_point[1][-1] == '0':
            num_with_point[1] = num_with_point[1][:-1]
        if len(num_with_point[1]) == 0:
            return str(num_with_point[0])
        else:
            return str(num_with_point[0]) + '.' + str(num_with_point[1])

    def to_number(self, num):
        newNum = num.split(",")
        newNum2 = ''
        for n in newNum:
            newNum2 += n
        return newNum2





