#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
from analyzable import *
import utils

class EchonestSong(Analyzable):
    """Class representing an Echonest Song (in very basic way).

    Attributes:
        id: id of the Echonest Song.

        name: name of the Echonest Song.

        preview_url: preview_url of the Echonest Song.
        
        features: :class:`.EchonestFeatures` of EchonestSong.
    """
    def __init__(
        self,
        id,
        name,
        preview_url,
        ):

        Analyzable.__init__(self, id)
        self.preview_url = preview_url
        self.name = name.encode('utf-8')
        self.type = 'echonest'

    def get_chromagram(self):

        directory = os.path.dirname(os.path.abspath(__file__))
        audio_file_path = directory + '/' + self.id + '.mp3'
        print "score is being downloaded"
        utils.download_file(self.preview_url, audio_file_path)
        print "file downloaded"
        chromagram = get_chromagram_from_audio(audio_file_path)
        utils.remove_file(audio_file_path)
        return chromagram

    def set_features(self, features):
        self.features = features
