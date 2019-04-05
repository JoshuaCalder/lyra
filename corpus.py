'''
This script gathers a training corpus of lyrics,
based on an input file of artists with 
artists being entered line-by-line

see example_artist_list.txt for an example input artist list

outputs lyrics to example_corpus.txt
'''

import lyricsgenius
import config		#contains genius api key

if __name__ == '__main__':
	artists = open('example_artist_list.txt').read().splitlines()
	print('Gathering lyrics from the following artists...\n')
	print(artists)

	f= open("RAPRAPRAP.txt","w+")

	for a in artists:
		genius = lyricsgenius.Genius(config.api_key)
		artist = genius.search_artist(a, max_songs=20, sort="popularity")
		if artist is not None:
			for s in artist.songs:
				song = genius.search_song(s.title, artist.name)
				if song is not None:
					f.write('###' + str(s.title) + '###' + str(artist.name) + '\n')
					f.write(song.lyrics)
					f.write('\n')
		else:
			print('Error: Artist not found: ' + str(a))		

	f.close()	