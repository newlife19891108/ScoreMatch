#!/usr/bin/python
# -*- coding: utf-8 -*-

score_id_list = [line.rstrip('\n') for line in open('../scores.txt')]
from apiwrappers.musescore import *
from apiwrappers.spotify import *
import os
from utils import *
from dtwmatcher.dtwmatch import *
from dtwmatcher.rank import *
from xml.dom import minidom
from apiwrappers.echonest import get_echonest_features_for_local_file
from unidecode import unidecode
import sys
import csv
tuples =[]
folder = '../out4/'
with open(folder+'rem.txt') as f:
    reader = csv.reader(f)
    for row in reader:
        tuples.append(row)
# tuples = [line.split(',') for line in
#           open('../out5/out.csv')]

from apiwrappers.musicdatatype import MusicDataType
for t in tuples:
    score_id = t[0]
    g_artist = t[1]
    g_title = t[2]
    try:
        title = minidom.parse(folder+score_id + '.xml'
                              ).getElementsByTagName('title'
                )[0].firstChild.nodeValue
    except AttributeError:
        title = ''
    try:
        subtitle = minidom.parse(folder + score_id + '.xml'
                                 ).getElementsByTagName('subtitle'
                )[0].firstChild.nodeValue
    except AttributeError:
        subtitle = ''
    try:
        composer = minidom.parse(folder + score_id + '.xml'
                                 ).getElementsByTagName('composer'
                )[0].firstChild.nodeValue
    except AttributeError:
        composer = ''
    try:
        poet = minidom.parse(folder+ score_id + '.xml'
                                 ).getElementsByTagName('poet'
                )[0].firstChild.nodeValue
    except AttributeError:
        poet = ''
    score = Score(
        score_id,
        title,
        subtitle,
        composer,
        poet,
        'n.mp3',
        'n.mp3',
        )
    f = open('results_m_poet_punc_spotify_norm_out4.csv', 'a')
    rem = open('rem.txt','a')
    # score = create_score(score_id)
    # result = score.metadata_match()

    method = 'M'
    result_score = 1
    queries = score.get_queries()
    for query in queries:
        template = get_echonest_features_for_local_file(folder+ score_id + '.mp3').chroma
        np.save(folder+'score/'+score_id,template)
        tracks = query_spotify(query[0])
        if tracks:
            ranking = []
            template = \
                get_echonest_features_for_local_file(folder + score_id + '.mp3').chroma
            for track in tracks:
                track_chroma = \
                    track.get_chromagram(MusicDataType.ECHONEST)
                np.save(folder+'audio/'+str(track.id),track_chroma)
            break

