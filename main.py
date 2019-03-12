import nltk 
import random

corpus = "\
There's a spider on the floor, on the floor.\
There's a spider on the floor, on the floor.\
Who could ask for anything more, than a spider on the floor.\
There's a spider on the floor, on the floor.\
Now the spider's on my leg, on my leg.\
Now the spider's on my leg, on my leg.\
Oh, I wish I had some Raid for this spider on my leg!\
Now the spider's on my leg, on my leg.\
Now the spider's on my chest, on my chest! \
Now the spider's on my chest, on my chest! \
Oh, I'd squish him in my vest, if it didn't make a mess! \
Now the spider's on my chest, on my chest!"

# https://sookocheff.com/post/nlp/ngram-modeling-with-markov-chains/
class Generator:
	def __init__(self):
		self.memory = {}

	def _learn_key(self, key, value):
		if key not in self.memory:
			self.memory[key] = []

		self.memory[key].append(value)

	def learn(self, text):
		tokens = text.split(" ")
		bigrams = [(tokens[i], tokens[i + 1]) for i in range(0, len(tokens) - 1)]	
		for bigram in bigrams:
			self._learn_key(bigram[0], bigram[1])

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

if __name__ == '__main__':
	g = Generator()
	g.learn(corpus)
	# print(g.memory)
	# for i in range(5):
	print(g.babble(5, "There's"))