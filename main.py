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
import re
import operator
import pronouncing
import config 		#contains genius api key

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
	line = []
	while(len(line) < 6):
		line = []
		word = random.choice(possible_rhymes)

		no_good_tags = ['PRT', 'DET', 'CONJ']
		rhyme_tag = nltk.pos_tag(word)[1]
		count = 0
		while rhyme_tag in no_good_tags and count < 20:
			word = random.choice(possible_rhymes)
			count += 1
		if word is None or count == 20:
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

def ngram(words, n=1):
	gram2 = dict()
	words = list(words)
	
	for i in range(len(words)-(n-1)):
		key = tuple(words[i:i+n])
		if key in gram2:
			gram2[key] += 1
		else:
			gram2[key] = 1

	gram = list(gram2.items())
	gram.sort(key=operator.itemgetter(1), reverse=True)
	# for i in range(20):
	# 	print(gram[i])
	return gram			

if __name__ == '__main__':
	f = open('rock_corpus.txt', 'r')
	txt = f.read()
	f.close()
	txt = re.sub("[\(\[].*?[\)\]]", "", txt)
	txt = re.sub("^###.*\n?", "", txt, flags=re.MULTILINE)
	words = re.split('[^A-Za-z\'.]+', txt.lower())
	filtered_words = filter(None, words) # Remove empty strings
	gram = ngram(filtered_words, 6)
	
	for i in range(8):
		starting_word = random.choice(words)
		last_word = generate_line_forward(starting_word, gram)
		possible_rhymes = pronouncing.rhymes(last_word)
		if len(possible_rhymes) == 0:
			generate_line_forward(random.choice(words), gram)
		else:
			generate_line_backward(possible_rhymes, gram)
