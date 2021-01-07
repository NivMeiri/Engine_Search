# #-------word to vec---------
# import  time
# from gensim.models import KeyedVectors
# filename = 'GoogleNews-vectors-negative300.bin'
# start=time.time()
# model = KeyedVectors.load_word2vec_format("C:/Users/Admin/Desktop/wordtovec/"+filename, binary=True)
# print(time.time()-start)
# result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
# print(result)
import spacy
# from nltk.corpus import wordnet
#
# def WordNet(word):
#     word_counter = 0
#     synonyms = []
#     for syn in wordnet.synsets(word):
#         for l in syn.lemmas():
#             if (word_counter < 2 and l.name not in synonyms):
#                 synonyms.append(l.name())
#                 word_counter += 1
#     return (set(synonyms))
# print(WordNet("shiri"))
#
#
import regex
word="shmulik"
word.isascii()