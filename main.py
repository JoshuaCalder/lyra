'''
This version uses a Markov Chain to model the text using bigrams.

After querying a lyric repository for matching song lyrics,
the lyrics are then tokenized and entered into memory as 
a 'bag of words'. 

When generating the next possible word, the most frequently 
occuring bigram is chosen. In case of a tie, a random bigram 
from among the most probabilistic next words is chosen

inspired by: http://www.samansari.info/2016/01/generating-sentences-with-markov-chains.html
'''

import sys, random
import nltk 
import lyricsgenius
import config #contains genius api key
import re
import operator
import pronouncing

# Bigram Markov chain inspired by: 
# sookocheff.com/post/nlp/ngram-modeling-with-markov-chains/
class Generator:
	def __init__(self):
		self.memory = {}

	# enters the bigram into memory if it isn't in memory already
	def _learn_key(self, key, value):
		if key not in self.memory:
			self.memory[key] = []

		self.memory[key].append(value)

	def learn(self, text):
		tokens = text.split(" ")
		bigrams = [(tokens[i], tokens[i + 1]) for i in range(0, len(tokens) - 1)]	
		for bigram in bigrams:
			self._learn_key(bigram[0], bigram[1])
		return random.sample(tokens, 1)[0]

	def _next(self, current_state):
		next_possible = self.memory.get(current_state)
		if not next_possible:
			next_possible = self.memory.keys()

		return random.sample(next_possible, 1)[0]

	def babble(self, amount, state=''):
		if not amount:
			return state
		next_word = self._next(state)
		return state + ' ' + self.babble(amount - 1, next_word)	

def clean_lyrics():
	'''
	TODO
		remove []
		remove ()
		remove ,
		remove .
		remove ###
		remove Madison: (things with colons afterwards)
	'''
	pass

# takes in filter object
def one_gram(words):
	# Create set of all unique words, this throws away any information about frequency however
	# corpus currently has 16105 unique words
	gram1 = dict()
	for w in words:
		if w in gram1:
			gram1[w] += 1
		else:
			gram1[w] = 1 

	gram1 = list(gram1.items())
	gram1.sort(key=operator.itemgetter(1), reverse=True)
	for i in range(20):
		print(gram1[i])

def two_gram(words):
	gram2 = dict()
	words = list(words)
	
	for i in range(len(words)-1):
		key = (words[i], words[i+1])
		if key in gram2:
			gram2[key] += 1
		else:
			gram2[key] = 1

	gram2 = list(gram2.items())
	gram2.sort(key=operator.itemgetter(1), reverse=True)
	# for i in range(20):
	# 	print(gram2[i])
	return gram2	

# https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
# weighted version of random.choice
def weighted_choice(choices):
	# gets total count of all choices
	total = sum(w for c, w in choices)
	# create uniform distribution (same probability)
	r = random.uniform(0, total)
	# example of choices (('not', 'anymore'), 10)
	upto = 0
	for c, w in choices:
		if upto + w > r:
			return c
		upto += w		

def print_line(line):
	count = 0
	for l in line:
		if count == len(line)-1:
			print(l, end=',')
		else:
			print(l, end=' ')
		count += 1
	print()	

def generate_line_forward(word, gram2):
	line = []
	for x in range(8):
		line.append(word)
		choices = [element for element in gram2 if element[0][0] == word]
		if not choices:
			break
		word = weighted_choice(choices)[1]
	print_line(line)
	return line[-1]

def generate_line_backward(possible_rhymes, gram2):
	rhyme_iterator = iter(possible_rhymes)
	line = []
	while(len(line) < 6):
		line = []
		word = next(rhyme_iterator, None)
		if word is None:
			print('.', end='')
			generate_line_forward(random.choice(possible_rhymes), gram2)
			break
		for x in range(8):
			line.insert(0, word)
			choices = [element for element in gram2 if element[0][1] == word]
			if not choices:
				break
			word = weighted_choice(choices)[0]
	if len(line) >= 6:
		print_line(line)

if __name__ == '__main__':
	f = open('rock_corpus.txt', 'r')
	txt = f.read()
	f.close()
	words = re.split('[^A-Za-z\'.]+', txt.lower())
	
	filtered_words = filter(None, words) # Remove empty strings
	gram2 = two_gram(filtered_words)
	
	for i in range(1):
		starting_word = random.choice(words)
		last_word = generate_line_forward(starting_word, gram2)
		possible_rhymes = pronouncing.rhymes(last_word)
		if len(possible_rhymes) == 0:
			generate_line_forward(random.choice(words), gram2)
		else:
			generate_line_backward(possible_rhymes, gram2)
		
	# g = Generator()
	# start_word = g.learn(get_lyrics(sys.argv[1]))	
	# print('\n\n**********************\n\n')
	# print('\nGenerated Song\n')
	# print(g.babble(40, start_word))