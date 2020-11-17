import timeit


import search_engine
import  parser_module
import numpy
import pandas as pd
from reader import ReadFile
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

if __name__ == '__main__':
    print( numpy.__version__)
    def infer_spaces(self,s):
        """Uses dynamic programming to infer the location of spaces in a string
        without spaces."""
        # Find the best match for the i first characters, assuming cost has
        # been built for the i-1 first characters.
        # Returns a pair (match_cost, match_length).
    # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
    '''
    def  Names_and_Entities( text):
        tokens = nltk.word_tokenize(text)
        print(tokens)
        pos=(nltk.pos_tag(tokens))
        print(pos)
        my_NE_word=nltk.ne_chunk(pos, binary=True)
        print(my_NE_word)
        
        

    
    
    #my_sent = "WASHINGTON -- In the wake of a string of abuses by New York police officers in the 1990s, Loretta E. Lynch, the top federal prosecutor in Brooklyn, spoke forcefully about the pain of a broken trust that African-Americans felt and said the responsibility for repairing generations of miscommunication and mistrust fell to law enforcement."






def get_continuous_chunks(text):
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
    return continuous_chunk


        '''


    def get_continuous_chunks(text):
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
        return continuous_chunk
my_sent="Donald Trump  is the best  president of United States"
Parser_1=parser_module.Parse()
print(Parser_1.parse_sentence("RT @ashtonpittman: Roughly ⅕ of the Mississippi Legislature, including the House speaker and Senate president, have tested positive for #CO…"))
#print(get_continuous_chunks(my_sent))

#search_engine.main()


