#!/usr/bin/python
# -*- coding: utf-8 -*-

from analyzable import *
import os
from utils import *
from echonest import get_echonest_features_for_url
from echonest import extract_artist_from_text
class Score(Analyzable):

    def __init__(
        self,
        id,
        title,
        subtitle,
        composer,
        mp3,
        midi,
        ):

        Analyzable.__init__(self, id)
        self.title = title
        self.composer = composer
        self.subtitle = subtitle
        self.mp3 = mp3
        self.midi = midi

    def get_chromagram(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        midi_file_path = directory + '/' + self.id + '.mid'
        download_file(self.midi, midi_file_path)
        chromagram = get_chromagram_from_midi(midi_file_path)
        remove_file(midi_file_path)
        return chromagram
    def get_echonest_analysis(self):
        return get_echonest_features_for_url(self.mp3)
    def get_search_query_for_score(self):
        return self.title + ' ' + self.composer
    def get_artist_from_echonest(self):
        query = self.title+" "+self.subtitle+" "+self.composer
        return extract_artist_from_text(query.lower())
