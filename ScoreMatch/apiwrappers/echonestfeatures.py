#!/usr/bin/python
# -*- coding: utf-8 -*-


class EchonestFeatures:
    """
        Class represents Echonest Features

        attributes:
            tempo: Tempo from the echonest analysis

            duration: Duration from the echonest analysis

            timesig: Time signature from the echonest analysis

            key: Key from the echonest analysis

            speechiness: Speechiness from the echonest analysis

            chroma: Chromagram from the echonest analysis

    """
    def __init__(self, feature_dict):
        self.tempo = feature_dict['tempo']
        self.duration = feature_dict['duration']
        self.timesig = feature_dict['time_signature']
        self.key = feature_dict['key']
        self.speechiness = feature_dict['speechiness']
        self.chroma = feature_dict['chroma']
