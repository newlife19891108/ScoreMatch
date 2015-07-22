import sys
import json
import urllib
import urlparse
from Track import *
from score import *
musescore_base = "http://api.musescore.com/services/rest/"
"score/json?oauth_consumer_key=KPAHk3xHbestkW8WsQ3ypwoXSnMVxE6z"
consumer_key="KPAHk3xHbestkW8WsQ3ypwoXSnMVxE6z"
def parseScore(data):
	metadata =  data["metadata"]
	title = metadata["title"]
	composer = metadata["composer"]
	subtitle = metadata["subtitle"]
	return title+ " " + composer
def getSearchQueryForScore(scoreid):
	url = musescore_base + "score/" + scoreid+".json?oauth_consumer_key="+consumer_key
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return parseScore(data)
def createScore(scoreid):
	url = musescore_base + "score/" + scoreid+".json?oauth_consumer_key="+consumer_key
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	id = scoreid
	secret = data["secret"]
	metadata = data["metadata"]
	title = metadata["title"]
	composer = metadata["composer"]
	subtitle = metadata["subtitle"]
	mp3 = "http://static.musescore.com/"+id+"/"+secret+"/score.mp3"
	midi = "http://static.musescore.com/"+id+"/"+secret+"/score.mid"
	return score(id,title,subtitle,composer,mp3,midi)