from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import requests
import urllib
import hashlib
from apiwrappers.echonest import *
def md5_for_file(f, block_size=2**7):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.digest()
# f = open('114295.mp3', 'rb')
# print hashlib.md5(f.read()).hexdigest()
# register_openers()
# url = 'http://developer.echonest.com/api/v4/track/upload'
# files = {'track': open('1142954.mp3', 'rb')}
# values = {'api_key': 'KAPGNMBNAIKKXKWG7','filetype':'mp3'}
# r = requests.post(url, files=files, data=values)
# response = r.json()
# print response
#t_id =  response['response']['track']['id']
get_echonest_song('1081066.mp3','score')
api_key = 'KAPGNMBNAIKKXKWG7'
#pytrack = track.track_from_filename('410.mp3')
