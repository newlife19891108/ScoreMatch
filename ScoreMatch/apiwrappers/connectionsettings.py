from utils import read_lines_from_file
import singleton
import sys
class ConnectionSettings(object):
    """Provides connection configurations for echonest and spotify apis.

    attributes:
        musescore_base:base url for echonest

        spotify_base:base url for spotify

        echonest_base:base url for echonest
    """

    __metaclass__ = singleton.Singleton
    echonest_key_path = '/Users/sekozer/Desktop/ScoreMatch/ScoreMatch/echonest.keys'
    musescore_key_path = '/Users/sekozer/Desktop/ScoreMatch/ScoreMatch/musescore.keys'
    def __init__(self):
        self.musescore_base = 'http://api.musescore.com/services/rest/'
        self.spotify_base = 'https://api.spotify.com/v1/'
        self.echonest_base = 'http://developer.echonest.com/api/v4/'

        self.set_echonest_key()
        self.set_musescore_key()

    def set_echonest_key(self):
        self.echonest_key = read_lines_from_file(ConnectionSettings.echonest_key_path)[0]
    def set_musescore_key(self):
        self.musescore_key = read_lines_from_file(ConnectionSettings.musescore_key_path)[0]