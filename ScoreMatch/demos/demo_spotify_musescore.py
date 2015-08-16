#!/usr/bin/python
# -*- coding: utf-8 -*-

from apiwrappers.musescore import *
from apiwrappers.spotify import query_spotify
import os
from utils import *
from dtwmatcher.dtwmatch import *
from dtwmatcher.rank import *
import sys
import numpy as np
def tempo_similarity(reference,query):
	tempos = np.array([reference/2,reference,reference*2])
	tempo_dif = tempos-np.array([query]*3)
	thresholds = [2.5,4,6]
	return (abs(tempo_dif)<thresholds).any()
	#print thresholds


s = create_score('1081216')
#s.extract_artist_song()
print s.get_queries()
tracks = query_spotify(s.title)
print len(tracks),"tracks are fetched"
ranking = rank_analyzables(s, tracks, 'full')

# midi_name = s.id + '.mid'
# template = s.id + '.csv'
# urllib.urlretrieve(s.midi, s.id + '.mid')
# get_chromagram_from_midi(midi_name, template)
# candidates = []
# # for track in tracks:
# #     file_name = track.id + '.mp3'
# #     urllib.urlretrieve(track.preview_url, track.id + '.mp3')
# #     os.system('sonic-annotator -t hpcp.n3 ' + file_name
# #               + ' -w csv --csv-force')
# #     csv_name = track.id + '_vamp_vamp-hpcp-mtg_MTG-HPCP_HPCP.csv'
# #     candidates.append(csv_name)
# # print rank(template, candidates, get_chromagram_from_csv,
# #            rdtw_subsequence_match_score)
i=1
for (el, score) in ranking:
	if tempo_similarity(s.tempo,el.tempo):
		str(i),el.name.encode('utf-8'), score,el.preview_url,el.uri,tempo_similarity(s.tempo,el.tempo),s.tempo,el.tempo
		i = i+1
