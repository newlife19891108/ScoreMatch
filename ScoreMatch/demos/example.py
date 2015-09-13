#!/usr/bin/python
# -*- coding: utf-8 -*-
from apiwrappers.musescore import *
from apiwrappers.spotify import *
import os
from utils import *
from dtwmatcher.dtwmatch import *
from dtwmatcher.rank import *
import os
from dtwmatcher.dtwmatch import *

audios = [each for each in os.listdir('.') if each.endswith('.mp3')]
candidates = [get_chromagram_from_audio(audio) for audio in audios]
# chroma_seq_1 = get_chromagram_from_audio(('./audio_samples/melody7.wav')
# chroma_seq_2 = get_chromagram_from_audio(('./audio_samples/melody8.wav')
# chroma_seq_3 = get_chromagram_from_audio(('./audio_samples/melody14.wav')
name = '1081376resampled.wav'
target = get_chromagram_from_audio(name)
audios = [a for a in audios if a!=name]
#target = chroma_seq_1
#candidates = [chroma_seq_3, chroma_seq_2]
res = []
for audio in audios:
	chro = get_chromagram_from_audio(audio)
	print audio
	score = rdtw_subsequence_match_score(target, chro)
	res.append((score,audio))
res.sort(key = lambda row: row[0])

for r in res:
	print r