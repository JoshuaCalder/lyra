'''
This version uses a Markov Chain to model the text using bigrams.

After scanning a corpus of song lyrics,
the lyrics are tokenized and entered into memory as 
a 'bag of words'. ex// [(('in', 'the'), 1413)]

When generating the next possible word, the most frequently 
occuring bigram is chosen. In case of a tie, a random bigram 
from among the most probabilistic next words is chosen

inspired by: http://www.samansari.info/2016/01/generating-sentences-with-markov-chains.html
'''

import sys, random
import nltk 
import re
import operator
import pronouncing
import config 		#contains genius api key
import pickle

# https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
# weighted version of random.choice
def weighted_choice(choices):
	# gets total count of all choices
	total = sum(c[1]['frequency'] for c in choices)

	# create uniform distribution (same probability)
	r = random.uniform(0, total)

	upto = 0
	for c in choices:
		if upto + c[1]['frequency'] > r:
			# return ngram tuple 
			return c[0]
		upto += c[1]['frequency']

'''
:return: generated line based on last rhyming word

Generates a line given a rhyming word, works backwords through ngram freq
'''
def generate_line_backward(word, gram):
	line = []
	for __ in range(8):	
		line.insert(0, word)
		choices = [element for element in gram if element[0][1] == word]
		if not choices:
			break
		word = weighted_choice(choices)[0]
	return line

'''
:return: generated line based on given starting word

Generates a line given a starting word, based on ngram frequencies
Example of choices:
If first word is 'up', then choices are (('up', 'i'), 3), (('up', 'you'), 2)
'''
def generate_line_forward(word, gram):
	line = []
	for __ in range(8):
		line.append(word)
		choices = [element for element in gram if element[0][0] == word]
		if not choices:
			break
		word = weighted_choice(choices)[1]
	return line

'''
:param gram: ngram tuple
:return: list of corresponding POS tags
'''
def get_gram_tags(gram):
	tags = []
	for g in gram:
		text = nltk.word_tokenize(g)
		tag = nltk.pos_tag(text)
		tags.append(tag[0][1])
	return tags		

'''
:param words: list of words to find n-gram frequency
:param n: str
:return: list of n-gram tuples

Generates a list of n-gram tuples
index 0: n-gram contents
index 1: n-gram frequency 
example of 2-gram: [(('in', 'the'), 1413)],
where the frequency of 'in the' occurs 1413 times
'''
def ngram(words, n):
	print('creating ngram...')
	gram2 = dict()
	
	for i in range(len(words)-(n-1)):
		key = tuple(words[i:i+n])
		if key in gram2:
			gram2[key]['frequency'] += 1
		else:
			gram_tags = get_gram_tags(key)
			gram2[key] = {
				'frequency': 1,
				'tags': gram_tags
			}
	for x in range(8):
		print(gram2[x])
	gram = list(gram2.items())

	return gram 

'''
:return: list containing cleaned text
Removes [], (), ### tags, empty strings
Also splits on alpha chars and forces lowercase on all words
'''
def text_cleaner(text):
	text = re.sub("[\(\[].*?[\)\]]", "", text)
	text = re.sub("^###.*\n?", "", text, flags=re.MULTILINE)
	words = re.split('[^A-Za-z\'.]+', text.lower())
	return list(filter(None, words)) # Remove empty strings

def create_gram_pickle(corpus):
	f = open(corpus, 'r')
	txt = f.read()
	f.close()

	filtered_words = text_cleaner(txt) 
	gram = ngram(filtered_words, n_gram)

	pickle_out = open('gram.pickle', 'wb')
	pickle.dump(gram, pickle_out)
	pickle_out.close()

def generate_lyrics(num_lines, filtered_words):
	lines = []
	line_len = 0
	for i in range(num_lines):
		# generate first line (no rhyming)
		if i % 2 == 0:
			while True:
				starting_word = random.choice(list(filter(None, filtered_words)))
				line = generate_line_forward(starting_word, gram)
				if len(line) == 8:
					lines.append(line)
					break
		# generate rhyming line		
		# if no rhyming line found, recreate first line (no rhyming)		
		else:
			rhyming_word = lines[-1][-1]
			possible_rhymes = pronouncing.rhymes(rhyming_word)
			while True:
				if len(possible_rhymes) == 0:
					return []
				rhyme = random.choice(possible_rhymes)
				rhyme_tag = nltk.pos_tag(rhyme)

				# remove particle, determine, and conjunction/coordinates
				bad_tags = ['RP', 'DT', 'CC']
				if rhyme_tag in bad_tags:
					possible_rhymes.remove(rhyme)
			
				line = generate_line_backward(rhyme, gram)
				if len(line) < 8:
					possible_rhymes.remove(rhyme)
				else:
					lines.append(line)
					break
	return lines			

if __name__ == '__main__':
	num_lines = int(sys.argv[1])	# number of lines the program generates
	n_gram = int(sys.argv[2]) 		# ngram count, set to 2 for bigram

	training_corpus = 'rap_corpus.txt'
	f = open(training_corpus, 'r')
	txt = f.read()
	f.close()

	filtered_words = text_cleaner(txt) 
	# create_gram_pickle(training_corpus) 
	
	pickle_in = open("gram.pickle","rb")
	gram = pickle.load(pickle_in)

	lines = generate_lyrics(num_lines, filtered_words)
	while len(lines) < num_lines:
		lines = generate_lyrics(num_lines, filtered_words)

	# print generated lyrics
	for line in lines:
		counter = 0
		for l in line:
			if counter == 7:
				print(l, end=',\n')
			else:		
				print(l, end=' ')
			counter += 1	