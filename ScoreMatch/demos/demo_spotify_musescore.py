#!/usr/bin/python
# -*- coding: utf-8 -*-

from apiwrappers.musescore import *
from apiwrappers.spotify import query_spotify
import os
from utils import *
from dtwmatcher.dtwmatch import *
from dtwmatcher.rank import *
from xml.dom import minidom
import utils
import sys
import numpy as np
import apiwrappers.spotify
import apiwrappers.echonest
def crop(query):
    for i,a in enumerate(query):
        query[i] = np.array([x if x >= 0.5 else 0 for x in a])
    return query
def findWholeExpression(w):
    return re.compile(r'\b({0})\b'.format(re.escape(w).encode('utf-8')), flags=re.IGNORECASE | re.UNICODE).search
def tempo_similarity(reference,query):
    tempos = np.array([reference/2,reference,reference*2])
    tempo_dif = tempos-np.array([query]*3)
    thresholds = [2.5,4,6]
    return (abs(tempo_dif)<thresholds).any()
    #print thresholds
import difflib

def matches(large_string, query_string, threshold):
    words = large_string.split()
    for word in words:
        s = difflib.SequenceMatcher(None, word, query_string)
        match = ''.join(word[i:i+n] for i, j, n in s.get_matching_blocks() if n)
        if len(match) / float(len(query_string)) >= threshold:
            yield match
score_id = '119363'
print utils.num_common_words('ali, veli','Ali, VE bugün')
try:
    title = minidom.parse('../out4/'+score_id+'.xml').getElementsByTagName('title')[0].firstChild.nodeValue
except AttributeError:
    title = ''
try:
    subtitle = minidom.parse('../out4/'+score_id+'.xml').getElementsByTagName('subtitle')[0].firstChild.nodeValue
except AttributeError:
    subtitle= ''
try:
    composer = minidom.parse('../out4/'+score_id+'.xml').getElementsByTagName('composer')[0].firstChild.nodeValue
except AttributeError:
    composer=''
try:
    poet = minidom.parse('../out4/'+score_id+'.xml').getElementsByTagName('poet')[0].firstChild.nodeValue
except AttributeError:
    poet=''


s = Score(score_id,title,subtitle,composer,poet,'502786.mp3','502786.mp3')
print title.encode('utf-8') + composer.encode('utf-8') + subtitle.encode('utf-8')+poet.encode('utf-8')
song = s.metadata_match()
if song!=None:
    print song.id,song.name,song.uri
sys.exit(0)
#s.extract_artist_song()
print s.get_queries()
tracks = query_spotify('snow connor miller')
print len(tracks),"hey ya!"
#ss = create_score('502786')
template = echonest.get_echonest_features_for_local_file('../out4/'+score_id+'.mp3').chroma
ranking = []
for track in tracks:
    print track.id
    track_chroma =  track.get_chromagram(MusicDataType.ECHONEST)
    if track_chroma!=None:
        print track.uri,track.artist
        points,beg,end = rdtw_global_match_score(template,track_chroma)
        ranking.append((track,points,beg,end,len(track_chroma)))
ranking.sort(key=lambda candidate: candidate[1])

#ranking = rank_analyzables(s, tracks, 'full')

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
templatelen = len(template)
for (el, score,beg,end,l) in ranking:
    print str(i),el.name.encode('utf-8'), score,el.preview_url,el.uri,el.artist,beg,end,l,templatelen
    i = i+1
