#!/usr/bin/python
# -*- coding: utf-8 -*-

from score import *
from connectionmanager import ConnectionManager
from connectionsettings import ConnectionSettings

"""
    This module provides wrappers for required muse score api functions
"""
def create_score(score_id):
    """
        create a score for given MuseScore score id

        Args:
            score_id: MuseScore id

        Returns:
            :class:`.Score` instance
    """
    cs = ConnectionSettings()
    base_url = cs.musescore_base + 'score/' + score_id + '.json?'
    params = {'oauth_consumer_key': cs.musescore_key}
    data = ConnectionManager().get_data(base_url,params)
    secret = data['secret']
    metadata = data['metadata']
    title = metadata['title']
    composer = metadata['composer']
    poet = metadata['poet']
    subtitle = metadata['subtitle']
    mp3 = 'http://static.musescore.com/' + score_id + '/' + secret \
        + '/score.mp3'

    midi = 'http://static.musescore.com/' + score_id + '/' + secret \
        + '/score.mid'
    return Score(
        score_id,
        title,
        subtitle,
        composer,
        poet,
        mp3,
        midi,
        )
