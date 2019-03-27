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
# Bigram Markov chain inspired by: 
# sookocheff.com/post/nlp/ngram-modeling-with-markov-chains/
# if __name__ == '__main__':
	# g = Generator()
	# start_word = g.learn(get_lyrics(sys.argv[1]))	
	# print('\n\n**********************\n\n')
	# print('\nGenerated Song\n')
	# print(g.babble(40, start_word))
	# 
# takes in filter object
def one_gram(words):
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