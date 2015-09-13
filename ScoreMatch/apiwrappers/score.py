#!/usr/bin/python
# -*- coding: utf-8 -*-

from analyzable import *
import os
import utils
from unidecode import unidecode
import echonest
from musicdatatype import MusicDataType
import spotify
import numpy as np
import re
import string


class Score(Analyzable):

    """This class represents a MuseScore Score

    Attributes:
        id: MuseScore id of the score

        title: title of the score

        subtitle: subtitle of the score

        composer: composer of the score

        mp3: mp3 of the score

        midi: midi of the score

        features: :class:`.EchonestFeatures` for the mp3 track of the score uplodaded to Echonest
    """

    def __init__(
        self,
        id,
        title,
        subtitle,
        composer,
        poet,
        mp3,
        midi,
        ):

        Analyzable.__init__(self, id)
        self.title = title
        self.composer = composer
        self.subtitle = subtitle
        self.mp3 = mp3
        self.midi = midi
        self.poet = poet

    def get_chromagram(self, mode=MusicDataType.AUDIO):
        """Get chromagram for the score

        Creates chromagram either from mp3,(:meth:`utils.get_chromagram_from_audio`) midi (:meth:`utils.get_chromagram_from_midi`) or echonest analysis(:meth:`apiwrappers.echonest.get_echonest_features_for_local_file`) of the score

        Args:
            mode: :class:`.MusicDataType`. 

        Returns:
            Chromagram np.array

        """

        directory = os.path.dirname(os.path.abspath(__file__))
        base_path = directory + '/' + self.id
        if mode == MusicDataType.AUDIO:
            audio_file_path = base_path + '.mp3'
            utils.download_file(self.mp3, audio_file_path)
            chromagram = get_chromagram_from_audio(audio_file_path)
        elif mode == MusicDataType.MIDI:
            midi_file_path = base_path + '.mid'
            utils.download_file(self.midi, midi_file_path)
            chromagram = utils.get_chromagram_from_midi(midi_file_path)
        elif mode == MusicDataType.ECHONEST:
            audio_file_path = base_path + '.mp3'
            utils.download_file(self.mp3, audio_file_path)
            self.features = \
                echonest.get_echonest_features_for_local_file(audio_file_path)
            chromagram = self.features.chroma
            np.savetxt(self.id + '.csv', chromagram)
            utils.remove_file(audio_file_path)
        return chromagram

    def get_metadata_text(self):
        return ' '.join([self.title, self.subtitle, self.composer,
                        self.poet])

    def get_queries(self):
        """Get list of queries from the metadata of the score for querying audio sources spotify or echonest

        The list of queries are created from title composer and subtitle of the score.
        From lower index to higher of the list strictness of the length and coverage of the query decreases and probability of finding results for the query increases:

        | strictness:query 
        | 0:title + composer + subtitle 
        | 1:title + composer + subtitle with stopwords removed
        | 2:title + composer
        | 3:title + composer with stopwords removed
        | 4:title
        | 5:title with stopwords removed

        | Identical queries with lower strictness removed from the list

        Returns:
            list of tuples (query,strictness)
        """

        tokens = [self.title, self.composer, self.subtitle]
        for token in tokens:
            token = ' '.join(token.split())
        queries = []
        query_temp = []
        j = 0
        for i in range(len(tokens), 0, -1):
            query = ' '.join(tokens[:i])
            query = utils.remove_multi_spaces_from_text(query)
            query = utils.normalize(query)
            if query not in query_temp:
                queries.append((query, 2 * j))
                query_temp.append(query)
            queryFiltered = utils.filter_text(query)
            if queryFiltered != query:
                queryFiltered = ' '.join(queryFiltered.split())
                if queryFiltered not in query_temp:
                    queries.append((queryFiltered, 2 * j + 1))
            j = j + 1
        return queries

    def findWholeExpression(self, w):
        return re.compile(r'\b({0})\b'.format(re.escape(w).encode('utf-8'
                          )), flags=re.IGNORECASE | re.UNICODE).search
    def removePunctuation(self,s):
        out = re.sub('[%s]' % re.escape(string.punctuation), '', s)
        return out
    def metadata_match(self):
        """Queries music sources by using the queries of :meth:`.get_queries` and return a song if its metadata is matching with metadata of the score.
        
        Returns:
            a :class:`.SpotifyTrack` or :class:`.EchonestSong` if there is a match
            None if there is no match
        """

        print '##metadata_match##'
        artists = self.get_artists_from_echonest()
        print artists
        print 'all artists extracted'
        text = self.get_metadata_text()
        text = utils.normalize(text)
        print 'search for songs..'
        for (artist_id, artist_name) in artists:
            songs = echonest.songs_by_artist_id(artist_id)
            songs.extend(spotify.songs_by_artist_name(artist_name))
            songs.extend(spotify.songs_by_artist_name2(artist_name))
            artist_name_decoded = utils.normalize(unidecode(artist_name).lower())
            comp_text = utils.token_remove(artist_name_decoded,
                    unidecode(text))
            #print "1:",text.encode('utf-8')
            #print "2:",comp_text.encode('utf-8')
            for song in songs:
                songtitle = utils.normalize(song.name)
                if self.composer !='':
                    composer_ = utils.normalize(self.composer)
                is_artist = artist_name_decoded in text or (self.composer!='' and composer_ in artist_name_decoded) or (self.composer!='' and artist_name_decoded in composer_) 
                if self.findWholeExpression(songtitle)(comp_text):

                    # is_song = utils.token_match(songtitle, comp_text)

                    is_song = True
                else:
                    is_song = False
                is_song = utils.token_match(self.removePunctuation(songtitle),self.removePunctuation(comp_text)) and len(songtitle.split())>0
                #or (self.title!='' and utils.normalize(self.title) in utils.normalize(songtitle))
                # print (self.title!=''  and self.title in songtitle),utils.normalize(self.title).encode('utf-8'),utils.normalize(songtitle).encode('utf-8')
                # print self.removePunctuation(songtitle).encode('utf-8'),self.removePunctuation(comp_text).encode('utf-8')
                print artist_name.encode('utf-8'),songtitle.encode('utf-8'),comp_text.encode('utf-8'),is_artist,is_song,song

                if is_song and is_artist:
                    print "name is ",songtitle.split()
                    return song
        return None

    def get_artists_from_echonest(self):
        """Get list of the artist for the metadata of the score from the echonest extractArtist method

        Returns:
            list of tuple(artist id, artist name)

        """

        query = self.get_metadata_text()
        query = utils.remove_multi_spaces_from_text(query)
        return echonest.extract_artist_from_text(query.lower())
