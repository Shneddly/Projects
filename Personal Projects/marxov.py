'''
This project helped me understand how markov chains work in NLP, using a corpus gathered from the text of Das Kapital.
Much of the markov code was pulled from a tutorial from https://www.kdnuggets.com/2019/11/markov-chains-train-text-generation.html
Comments by me to show what each snippet is doing
'''

'''
This section creates a corpus of text by reading from text files in a given directory
'''
import os
os.chdir('Kapital Texts/')
corpus = ''
for file_name in os.listdir():
    f = open(file_name,'r',encoding='utf-8')
    corpus += f.read()
    f.close()

'''
Because of the formatting of the text files, this section cleans up and removes unneeded characters,
or tokens, and ensures that all punctuation is separated by white space
'''

import re
corpus = corpus.replace('\n',' ')
corpus = corpus.replace('\t',' ')
corpus = corpus.replace('\xa0',' ')
corpus = corpus.replace('&c','etc')
corpus = corpus.replace('     ',' ')
corpus = corpus.replace('    ',' ')
corpus = corpus.replace('   ',' ')
corpus = corpus.replace('  ',' ')
corpus = corpus.replace('"',' " ')
corpus = corpus.replace('“',' " ')
corpus = corpus.replace('”',' ” ')
for spaced in ['.',',','-','!','?','(',')',':']:
    corpus = corpus.replace(spaced,f' {spaced} ')
corpus = re.sub(r'\[\d+\]','',corpus)

'''
This section creates a list of words, and a list of unique words, from the dataset.
'''
# split the text corpus into words using whitespace
corpus_words = corpus.split(' ')
# remove empty strings from the list
corpus_words = [word for word in corpus_words if word != '']
# create a list from the set of all words, in effect all unique words
distinct_words = list(set(corpus_words))
# create a count of all distinct words
distinct_words_count = len(distinct_words)
# create a dictionary from all unique words, and assign an id number
word_idx_dict = {word: i for i, word in enumerate(distinct_words)}

#distinct_words_count

import scipy
from scipy.sparse import dok_matrix

k = 3 # adjustable
# create a list of all phrases of length k from the list of all words
sets_of_k_words = [ ' '.join(corpus_words[i:i+k]) for i, _ in enumerate(corpus_words[:-k]) ]
# create a list of all unique phrases from the list of all phrases
distinct_sets_of_k_words = list(set(sets_of_k_words))
# create a count of all unique phrases from the list of all phrases
sets_count = len(distinct_sets_of_k_words)

# create a Dictionary of Keys based sparse matrix with initial shape M,N
next_after_k_words_matrix = dok_matrix((sets_count, distinct_words_count))
# create a dictionary from all unique phrases, and assign an id number
k_words_idx_dict = {word: i for i, word in enumerate(distinct_sets_of_k_words)}

# start a for loop to enumerate through the list of all phrases
for i, word in enumerate(sets_of_k_words[:-k]):
    # assign an internal variable to the id number of the current phrase
    word_sequence_idx = k_words_idx_dict[word]
    # assign an internal variable to the id number of the word following the current phrase
    next_word_idx = word_idx_dict[corpus_words[i+k]]
    # on the row and column of the matrix matching the previous id nums,
    # increase the value by one
    # this uses the matrix to enumerate the number of times a given word follows
    # a given word sequence
    next_after_k_words_matrix[word_sequence_idx, next_word_idx] +=1

'''
This takes in a list of objects, and a list of weights, 
and returns a random object based on the given weights.
'''

import numpy as np
import random
from random import random 

def weighted_choice(objects, weights):
    """ returns randomly an element from the sequence of 'objects', 
        the likelihood of the objects is weighted according 
        to the sequence of 'weights', i.e. percentages."""

    # convert list of weights to float64 array
    weights = np.array(weights, dtype=np.float64)
    # create a sum of the weights
    sum_of_weights = weights.sum()
    # standardization:
    # standardize the weights array by multiplying it by the inverse
    # of the weights sum, and output to weights
    # this ensures that weights all add to 1
    np.multiply(weights, 1 / sum_of_weights, weights)
    # set weights to a cumulative sum of the array,
    # so the last item is 1.0, the second to last is 1.0-(probability of last), etc
    # needs to be this way for the for loop to function
    weights = weights.cumsum()
    # assign a variable to a random number between 0.0 and 1.0
    x = random()
    # use a for loop to find the weight in the weights array that approx. matches the random number x,
    # then return the object from the objects array that corresponds to that weight
    for i in range(len(weights)):
        if x < weights[i]:
            return objects[i]

def sample_next_word_after_sequence(word_sequence, alpha = 0):
    # given an input of a word sequence
    # assign an internal variable to the vector associated with
    # the word sequence id in the sparse matrix
    next_word_vector = next_after_k_words_matrix[k_words_idx_dict[word_sequence]] + alpha
    # assign an internal variable with the vector of probabilities of each word
    likelihoods = next_word_vector/next_word_vector.sum()
    # use the weighted choice function to return a weighted random next word
    return weighted_choice(distinct_words, likelihoods.toarray())
    #return random.choices(distinct_words, likelihoods.toarray())
    
def stochastic_chain(seed, chain_length=15, seed_length=2):
    # given a seed phrase, a chain length, and a seed length
    # split the seed phrase into separate words
    # and check to make sure it matches the seed length
    current_words = seed.split(' ')
    if len(current_words) != seed_length:
        raise ValueError(f'wrong number of words, expected {seed_length}')
    # initialize the output sentence with the seed phrase
    sentence = seed
    # using the chain length, create a for loop
    for _ in range(chain_length):
        # add whitespace to the sentence
        sentence += ' '
        # get the next word using the custom function, given a string of the current_words
        next_word = sample_next_word_after_sequence(' '.join(current_words))
        # append the next word onto the sentence
        sentence += next_word
        # change current_words to shift one word over
        current_words = current_words[1:]+[next_word]
    return sentence
# example use    
print(stochastic_chain('Now let us',chain_length=100,seed_length=3))
