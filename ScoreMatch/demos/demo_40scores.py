#!/usr/bin/python
# -*- coding: utf-8 -*-
score_id_list = [line.rstrip('\n') for line in open('../scores.txt')]
from apiwrappers.musescore import *
for score_id in score_id_list:
    score = create_score(score_id)
    print ','.join(["title:"+score.title.encode('utf-8'), "composer:"+score.composer.encode('utf-8'), "subtitle:"+score.subtitle.encode('utf-8')])
    print score.get_artist_from_echonest()