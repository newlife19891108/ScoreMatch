#!/usr/bin/python
# -*- coding: utf-8 -*-
import dtwMatch
import chromagram

chroma_seq_1 = get_chromagram('./audio_samples/melody7.wav')
chroma_seq_2 = get_chromagram('./audio_samples/melody8.wav')
chroma_seq_3 = get_chromagram('./audio_samples/melody14.wav')

target = chroma_seq_1
candidates = [chroma_seq_3, chroma_seq_2]
scores = []
for candidate in candidates:
    score = dtw_global_match_score(target, candidate)
    scores.append(score)
