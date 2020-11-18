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
        text_tokensterm = []
        ##todo clean the words after text re , . & |
        list_of_words = text.split(" ")
        list_of_words = [w.lower() for w in list_of_words if w not in self.stop_words]
        for i in range(0, len(list_of_words)):
            if len(list_of_words[i]) > 0:
                ###hash tag law
                if list_of_words[i][0] == "#":
                    text_tokensterm.append(list_of_words[i])
                    self.parse_tags(list_of_words[i][1:-1], text_tokensterm)

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
        tokenized_text = self.parse_sentence(full_text)
        print(tokenized_text)
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
            text_tokensterm.append(term)
        elif (term.islower()):
            hash_list = self.infer_spaces(term)
            for hash in hash_list:
                text_tokensterm.append(hash)
        else:
            hash_list = re.findall('[A-Z][^A-Z]*', term)
            for hash in hash_list:
                text_tokensterm.append(hash)


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