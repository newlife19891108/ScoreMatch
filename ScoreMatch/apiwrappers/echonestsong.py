#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
from analyzable import *


class EchonestSong(Analyzable):

    def __init__(
        self,
        id,
        name,
        preview_url,
        ):
        Analyzable.__init__(self, id)
        self.preview_url = preview_url
        self.name = name
    def get_chromagram(self):

        directory = os.path.dirname(os.path.abspath(__file__))
        audio_file_path = directory + '/' + self.id + '.mp3'
        download_file(self.preview_url, audio_file_path)
        chromagram = get_chromagram_from_audio(audio_file_path)
        remove_file(audio_file_path)
        return chromagram
    def set_features(self,tempo,duration,timesig,key,chroma):
    	self.tempo = tempo
    	self.duration = duration
    	self.timesig = timesig
    	self.key = key
        self.chroma = chroma
    def get_echonest_analysis(self):
        
        return self.chroma,self.timesig,self.key,self.duration,self.tempo