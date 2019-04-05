import nltk 
import random
import ast
import operator

# Returns tag sets that meet a certain threshold for appearing in the corpus
def get_highest_tag_freq( txtfile, threshold ):
	f = open( txtfile, 'r' )
	lines = f.readlines()
	tagset_list = []
	
	tag_freq = {}
	for line in lines:
		if line in tag_freq:
			tag_freq[line] += 1
		else:
			tag_freq[line] = 1

	tag_freq_min_2 = {}
	for k,v in tag_freq.items():
		if v > threshold:
			tag_freq_min_2[k] = v
	
	f.close()
	return tag_freq_min_2

# Returns lst of POS tags in the input line
def get_tagset( line ):
	if line[0].isalpha() and len( line.split() ) > 6:
		text = nltk.word_tokenize( line )
		tags = nltk.pos_tag( text )
		tag_set = []
		for tag in tags:
			tag_set.append( tag[1] )
		return tag_set
	else: 
		return None

# Creates list of all POS tags contained in provided text file
# Takes some time
def generate_tagset( txtfile ):
	f = open( txtfile, 'r' )
	lines = f.readlines()
	tagset_list = []
	for line in lines:
		tagset = get_tagset( line )	
		if tagset is not None:
			print(tagset)
	f.close()	

def print_dict(d, iters):
	count = 0
	for k,v in d.items():
		if count < iters:
			print(str(k) + str(v))
		count += 1	

if __name__ == '__main__':
	# generate_tagset('rap_corpus_small.txt')
	
	sorted_tag_freq = get_highest_tag_freq( 'raptags.txt', 5)
	print_dict(sorted_tag_freq, 20)


	