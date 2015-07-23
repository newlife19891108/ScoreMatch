#!/usr/bin/python
# -*- coding: utf-8 -*-

from apiwrappers.musescore import *
import apiwrappers.track
from apiwrappers.spotify import *
import os
from utils import *
from dtwmatcher.dtwmatch import *
from dtwmatcher.rank import *

s = create_score('114295')
query = s.get_search_query_for_score()
tracks = query_spotify(query)
chromascore = s.get_chromagram()
ranking = rank_analyzables(s, tracks, rdtw_subsequence_match_score)

midi_name = s.id + '.mid'
template = s.id + '.csv'
urllib.urlretrieve(s.midi, s.id + '.mid')
get_chromagram_from_midi(midi_name, template)
candidates = []
for track in tracks:
    file_name = track.id + '.mp3'
    urllib.urlretrieve(track.preview_url, track.id + '.mp3')
    os.system('sonic-annotator -t hpcp.n3 ' + file_name
              + ' -w csv --csv-force')
    csv_name = track.id + '_vamp_vamp-hpcp-mtg_MTG-HPCP_HPCP.csv'
    candidates.append(csv_name)
print rank(template, candidates, get_chromagram_from_csv,
           rdtw_subsequence_match_score)
for (el, score) in ranking:
    print el.name, score
