import networkx as nx
import matplotlib.pyplot as plt
import nltk
import re
from nltk.tokenize import word_tokenize
import pprint
import random

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

if __name__ == '__main__':
	training_corpus = 'rap_corpus.txt'
	bigram_list = []

	with open(training_corpus) as f:
		lines = f.readlines()

	for line in lines:
		cleaned_line = text_cleaner(line)
		if len(cleaned_line) > 0:
			bigram = nltk.bigrams(cleaned_line)
			tag = nltk.pos_tag(cleaned_line)
			tupee = list(zip(bigram, tag))
			for t in tupee:
				# print(t)
				bigram_list.append(t)

	G = nx.MultiDiGraph()

	G.add_edges_from(bigram_list)

	# nx.draw(G, with_labels=True, font_weight='bold')
	# plt.show()

	# print(list(G.neighbors('hi')))
	# print(list(G.nodes))
	curr_node = random.choice(G.nodes())
	print(curr_node)
	for __ in range(4):
		curr_word = random.choice(list(G.neighbors(curr_node)))
		print(curr_word)