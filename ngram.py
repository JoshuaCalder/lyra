import argparse
import re
import nltk
import pickle

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
	print('this could take a few minutes')
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

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("training_corpus", help=".txt of lyric training corpus", type=str)
	parser.add_argument("output_pickle", help="name of .pickle file to store n-gram model in", type=str)
	parser.add_argument("n_gram", help="ngram count, ie. set to 2 for bigram", type=int)
	args = parser.parse_args()

	f = open(args.training_corpus, 'r')
	txt = f.read()
	f.close()

	filtered_words = text_cleaner(txt) 

	gram = ngram(filtered_words, args.n_gram)

	pickle_out = open(args.output_pickle, 'wb')
	pickle.dump(gram, pickle_out)
	pickle_out.close()
	print(str(args.output_pickle) + ' was succesfully created using a ' + str(args.n_gram) + '-gram model') 