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
with open('../out9/out.csv') as f:
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
        title = minidom.parse('../out9/' + score_id + '.xml'
                              ).getElementsByTagName('title'
                )[0].firstChild.nodeValue
    except AttributeError:
        title = ''
    try:
        subtitle = minidom.parse('../out9/' + score_id + '.xml'
                                 ).getElementsByTagName('subtitle'
                )[0].firstChild.nodeValue
    except AttributeError:
        subtitle = ''
    try:
        composer = minidom.parse('../out9/' + score_id + '.xml'
                                 ).getElementsByTagName('composer'
                )[0].firstChild.nodeValue
    except AttributeError:
        composer = ''
    try:
        poet = minidom.parse('../out9/' + score_id + '.xml'
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
    f = open('results_m_poet_punc_spotify_norm_out3.csv', 'a')
    rem = open('rem.txt','a')
    #score = create_score(score_id)
    result = score.metadata_match()

    method = 'M'
    result_score = 1
    # if result == None:
    #     queries = score.get_queries()
    #     print queries
    #     print 'queries generated for ', score_id
    #     for query in queries:
    #         tracks = query_spotify(query[0])
    #         print len(tracks), 'tracks downloaded for ', score_id
    #         order = query[1]
    #         if tracks:
    #             print 'tracks will be ranked '
    #             ranking = []
    #             template = \
    #                 get_echonest_features_for_local_file('../out5/'
    #                     + score_id + '.mp3').chroma
    #             for track in tracks:
    #                 track_chroma = \
    #                     track.get_chromagram(MusicDataType.ECHONEST)
    #                 if track_chroma != None:
    #                     points = rdtw_global_match_score(template,
    #                             track_chroma)
    #                     ranking.append((track, points))

    #             # ranking = rank_analyzables(score, tracks, 'full')

    #             print 'tracks are ranked'
    #             ranking = [(el, sco) for (el, sco) in ranking
    #                        if el.echonest_features.speechiness < 0.8]

    #             if ranking != []:
    #                 ranking.sort(key=lambda candidate: candidate[1])
    #                 best = ranking[0][0]
    #                 best_score = ranking[0][1]
    #             else:
    #                 best = None
    #             result = best
    #             result_score = best_score
    #             method = 'A' + str(order) + '-' + str(len(tracks))
    #             break
    if result == None:
        print 'nomatch'
        f.write(score_id + ',' + g_title + ',' + g_artist + ',' + ','
                + ',' + ',' + ',' + ',' + ',' + '\n')
        rem.write(score_id+','+g_title+','+g_artist+'\n')
    else:   
        print 'metadata match for', score_id
        title = result.name
        title = title.replace(',', ' ')
        result_artist = result.artist
        if result.type == 'spotify':
            uri = result.uri
        else:
            uri = 'echonest...'
        print title.encode('utf8'),result_artist.encode('utf8')
        f.write(score_id + ',' + g_title + ',' + g_artist + ','
                + result.id + ',' + title.encode('utf-8') + ',' + unidecode(result_artist)+ ','
                + result.type + ',' + method + ',' + uri + ','
                + str(result_score) + '\n')
        f.close()
