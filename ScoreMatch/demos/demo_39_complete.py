#!/usr/bin/python
# -*- coding: utf-8 -*-

score_id_list = [line.rstrip('\n') for line in open('../scores.txt')]
from apiwrappers.musescore import *
from apiwrappers.spotify import *
import os
from utils import *
from dtwmatcher.dtwmatch import *
from dtwmatcher.rank import *
from unidecode import unidecode
i = 0


def tempo_similarity(reference, query):
    tempos = np.array([reference / 2, reference, reference * 2])
    tempo_dif = tempos - np.array([query] * 3)
    thresholds = [2.5, 4, 6]
    return (abs(tempo_dif) < thresholds).any()


for score_id in score_id_list:
    f = open('results.csv', 'a')

    score = create_score(score_id)
    print score.title

    # result = score.extract_artist_song()

    method = 'M'
    result = None
    if result == None:

        queries = score.get_queries()
        print 'queries generated for ', score_id
        for query in queries:
            tracks = query_spotify(query[0])
            print len(tracks), 'tracks downloaded for ', score_id
            order = query[1]
            if tracks:
                print 'tracks will be ranked '
                ranking = rank_analyzables(score, tracks, 'full')
                print 'tracks are ranked'
                ranking = [(el, sco) for (el, sco) in ranking
                           if el.echonest_features.speechiness < 0.8]
                if ranking != []:
                    best = ranking[0][0]
                else: 
                    best = None
                result = best
                method = 'A' + str(order) + '-' + str(len(tracks))
                break
    if result == None:
        print 'nomatch'
        f.write(score.id + ',' + score.title + ',' + 'nomatch' + ','
                + 'nomatch' + ',' + 'nomatch' + ',' + 'nomatch' + '\n')
    else:
        print 'metadata match for', score_id
        title = result.name
        title = title.replace(',', ' ')
        title = unidecode(title)

        if result.type == 'spotify':
            uri = result.uri
        else:
            uri = 'echonest...'
        print result.id, title, result.type
        f.write(score_id + ',' + unidecode(score.title) + ','
                + result.id + ',' + title + ',' + result.type + ','
                + method + ',' + uri + '\n')
        f.close()
