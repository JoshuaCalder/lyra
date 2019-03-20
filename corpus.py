'''
This script is used to gather a massive training corpus 
of hip hop lyrics, based on artists in rapper_list.txt
'''
import lyricsgenius
import config #contains genius api key

if __name__ == '__main__':
	artists = open('rock_list_small.txt').read().splitlines()
	print(artists)

	f= open("corpus_rock2.txt","w+")

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