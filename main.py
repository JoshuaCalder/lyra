'''
This version uses a Markov Chain to model the text using bigrams.

After querying a lyric repository for matching song lyrics,
the lyrics are then tokenized and entered into memory as 
a 'bag of words'. 

When generating the next possible word, the most frequently 
occuring bigram is chosen. In case of a tie, a random bigram 
from among the most probabilistic next words is chosen
'''

import sys, random
import nltk 
import lyricsgenius
import config #contains genius api key

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

def get_lyrics(artist_name):
	lyrics = ''
	genius = lyricsgenius.Genius(config.api_key)
	artist = genius.search_artist(artist_name, max_songs=5, sort="title")
	for s in artist.songs:
		song = genius.search_song(s.title, artist.name)
		lyrics += song.lyrics
	return lyrics

if __name__ == '__main__':
	if len(sys.argv) < 1:
		print('Please provide an artist name as input')
		sys.exit(1)	
	g = Generator()
	start_word = g.learn(get_lyrics(sys.argv[1]))	
	print('\n\n**********************\n\n')
	print('\nGenerated Song\n')
	print(g.babble(20, start_word))