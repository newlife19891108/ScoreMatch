#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import nltk
import sys
score_id_list = [line.rstrip('\n') for line in open('../scores.txt')]
from apiwrappers.musescore import *
import string

def get_number_of_tracks_1(query):
	query = query.encode('utf-8')
	query = query.replace('|', ' ')
	query = " ".join(query.split())
	tracks = query_spotify(query)
	query = re.sub(',', ' ', query)

	return (query,str(len(tracks)))
def get_number_of_tracks_2(query):
	query = query.encode('utf-8')
	#query = query.translate(string.maketrans("",""), string.punctuation)
	query = re.sub('\(.*\)', '', query)
	query = re.sub('\d{4}','',query)
	query = query.replace('|', ' ')

	stop = set(())
	query = " ".join([word for word in query.split() if word.lower() not in stop])
	tracks = query_spotify(query)
	query = re.sub(',', ' ', query)

	return (query,str(len(tracks)))

f = open('numoftracks', 'w')
f2= open('results.csv','w')
i=0
tuples = []
for score_id in score_id_list:
	if i>=3:
		i=i+1
		breal
	score = create_score(score_id)
	print ','.join(['title:' + score.title.encode('utf-8'), 'composer:'
				   + score.composer.encode('utf-8'), 'subtitle:'
				   + score.subtitle.encode('utf-8')])
	strr  = score.title+" "+score.composer+" "+score.subtitle
	song,artist =  extract_artist_from_text(score.title,score.composer,score.subtitle)
	song = 	re.sub(',', ' ', song)
	song = " ".join(song.split())
	artist = re.sub(',', ' ', artist)
	artist = " ".join(artist.split()	)
	print song,":",artist
	score_info = score.title.encode('utf-8')+" "+score.composer.encode('utf-8')+score.subtitle.encode('utf-8')
	score_info = " ".join(score_info.split())
	score_info = re.sub(',',' ',score_info)
	f2.write(score_info +","+artist+","+song+"\n")
	# # score.get_tokens()
	# f.write(score_id)
	# q,w =  get_number_of_tracks_1(score.title)
	# f.write(","+q+","+w)
	# q,w = get_number_of_tracks_1(score.title + ' ' + score.composer)
	# f.write(","+q+","+w)	
	# q,w = get_number_of_tracks_1(score.title + ' ' + score.composer
	# 								 + ' ' + score.subtitle)
	# f.write(","+q+","+w)
	# q,w = get_number_of_tracks_2(score.title)
	# f.write(","+q+","+w)
	# q,w = get_number_of_tracks_2(score.title + ' ' + score.composer)
	# f.write(","+q+","+w)
	# q,w = get_number_of_tracks_2(score.title + ' ' + score.composer
	# 							 + ' ' + score.subtitle)
	# f.write(","+q+","+w)



	# #f.write(score_id + ',' +score.title.encode('utf-8') +',' +str(num_1_1) + ',' + str(num_1_2) + ','
	# 		#+ str(num_1_3)+','+str(num_2_1) + ',' + str(num_2_2) + ','+ str(num_2_3)+"\n")
	# f.write("\n")
f.close()
f2.close()

	# print score.get_artist_from_echonest()
