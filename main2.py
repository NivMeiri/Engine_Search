#-------word to vec---------
import  time
from gensim.models import KeyedVectors
filename = 'GoogleNews-vectors-negative300.bin'
start=time.time()
model = KeyedVectors.load_word2vec_format("C:/Users/Admin/Desktop/wordtovec/"+filename, binary=True)
print(time.time()-start)
result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
print(result)