#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import urllib
import urlparse
from score import *
musescore_base = 'http://api.musescore.com/services/rest/'
consumer_key = 'KPAHk3xHbestkW8WsQ3ypwoXSnMVxE6z'


def create_score(score_id):
    url = musescore_base + 'score/' + score_id \
        + '.json?oauth_consumer_key=' + consumer_key
    print url
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    id = score_id
    secret = data['secret']
    metadata = data['metadata']
    title = metadata['title']
    composer = metadata['composer']
    subtitle = metadata['subtitle']
    mp3 = 'http://static.musescore.com/' + id + '/' + secret \
        + '/score.mp3'

    midi = 'http://static.musescore.com/' + id + '/' + secret \
        + '/score.mid'
    return Score(
        id,
        title,
        subtitle,
        composer,
        mp3,
        midi,
        )
