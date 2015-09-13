import spotipy
import requests
import musicbrainzngs
import re
import urllib
import csv
sp = spotipy.Spotify()

apikey = 'musichackday2014'
endpoint = 'http://api.musescore.com/services/rest/score'
format = 'json'

def createSearchString(score):
    searchString = ""
    if score['metadata']['composer']:
        searchString += score['metadata']['composer'] + " "
    if score['metadata']['poet']:
        searchString += score['metadata']['poet'] + " "
    if score['title']:
        searchString += score['title'] + " "
    if score['metadata']['title']:
        searchString += score['metadata']['title'] + " "
    if score['metadata']['subtitle']:
        searchString += score['metadata']['subtitle'] + " "
    if score['description']:
        searchString += score['description'] + " "
    if score['tags']:
        searchString += score['tags'].replace(",", " ")
    searchString = searchString.strip()
    return searchString

def wordsCount(s):
    return len(s.split(" "))

def findWholeExpression(w):
    return re.compile(r'\b({0})\b'.format(re.escape(w).encode('utf-8')), flags=re.IGNORECASE | re.UNICODE).search

def findMatchSpotify(text, scoreComposer, searchString, scoreid):
    results = sp.search(q=text, limit=5)
    # remove title from search string
    lText = text.lower()
    lSearchString = searchString.lower()
    escText = re.escape(text)
    regex = re.compile(r'\b('+escText+r')\b', flags=re.IGNORECASE | re.UNICODE)
    lSearchString = regex.sub("", lSearchString)
    lScoreComposer = scoreComposer.lower()
    for i, t in enumerate(results['tracks']['items']):
        #print ' ', i, t['name'], t['artists'][0]['name']
        #find artist in search string
        artist = t['artists'][0]['name']
        lArtist = artist.lower()
        if findWholeExpression(lArtist)(lSearchString) or (lScoreComposer != "" and (findWholeExpression(lScoreComposer)(lArtist) or findWholeExpression(lArtist)(lScoreComposer))) :
              #print "MATCH ", scoreid, t['name'] + " - " + artist
              #print "MATCH artist " + t['artists'][0]['uri']
              #print "MATCH track " + t['uri']
              return (scoreid, artist.encode("utf-8"), t['artists'][0]['uri'], t['name'].encode("utf-8"), t['uri'], 1.0)
    return None

def matchTitleOnlySpotify(title, scoreid):
    results = sp.search(q=title, limit=1)
    # remove title from search string
    lTitle = title.lower()
    for i, t in enumerate(results['tracks']['items']):
        print ' ', t['name']
        lSpotifyTitle = t['name'].lower()
        # do not match too short title
        if wordsCount(lSpotifyTitle) <= 3:
            continue
        if findWholeExpression(lSpotifyTitle)(lTitle) or findWholeExpression(lTitle)(lSpotifyTitle) :
              artist = t['artists'][0]['name']
              #print "MATCH TrACK ONLY", scoreid, t['name'] + " - " + artist
              #print "MATCH artist " + t['artists'][0]['uri']
              #print "MATCH track " + t['uri']
              return (scoreid, artist.encode("utf-8"), t['artists'][0]['uri'], t['name'].encode("utf-8"), t['uri'], 0.5)
    return None

def findMatchMB(text, scoreComposer, searchString, scoreid):
    results = musicbrainzngs.search_recordings(query=text, limit=5)
    # remove title from search string
    lText = text.lower()
    lSearchString = searchString.lower()
    regex = re.compile(r'\b('+text+r')\b', flags=re.IGNORECASE)
    lSearchString = regex.sub("", lSearchString)
    for i, t in enumerate(results['recording-list']):
        #print t['artist-credit'][0]['artist']['name']
        artist = t['artist-credit'][0]['artist']['name']
        lArtist = artist.lower()
        if lSearchString.find(lArtist) >= 0 or (scoreComposer != "" and lArtist.find(scoreComposer) >= 0) :
              print "MATCH ", scoreid, t['title'] + " - " + artist
              #print "MATCH artist " + t['artists'][0]['uri']
              #print "MATCH track " + t['uri']
              return (scoreid, artist.encode("utf-8"), t['artist-credit'][0]['artist']['uri'], t['title'].encode("utf-8"), t['uri'])
    return None

def processScore(score):
    scoreid = score['id']
    url = endpoint + "/" + str(scoreid) + '.' +format + '&oauth_consumer_key=' + apikey
    r = requests.get(url)
    score = r.json()
    searchString = createSearchString(score)
    
    print scoreid
    #print score["title"]

    scoreComposer = score["metadata"]["composer"]
    if scoreComposer is None:
        scoreComposer = ""
    
    result = findMatchSpotify(score["title"], scoreComposer, searchString, scoreid) 
    if result:
        return result
    if score['metadata']['title']: 
        result = findMatchSpotify(score['metadata']['title'], scoreComposer, searchString, scoreid)
        if result:
            return result
    if wordsCount(score["title"]) > 3 :
        result = matchTitleOnlySpotify(score["title"], scoreid)
        if result:
            return result
    if score['metadata']['title'] and wordsCount(score['metadata']["title"]) > 3 :
        result = matchTitleOnlySpotify(score['metadata']['title'], scoreid)
        if result:
             return result
    return None
def processCSV(csv):
    lines = open(csv).readlines()
    for line in lines
        id_ = line.strip()
def processPages(text=""):
    total = 0
    match = 0
    f = open("output.csv", "wb")
    writer = csv.writer(f)
    for page in xrange(0,100):
        url = endpoint  + '.' +format + '&oauth_consumer_key=' + apikey + '&page=' + str(page) + '&text=' + urllib.quote(text)
        r = requests.get(url)

        scores = r.json()
        
        print str(page) + " - " + str(len(scores))
        for score in scores:
            #print scoreid
            #get a score
            result = processScore(score)
            if result: 
                print result
                writer.writerow(result)   
                match+=1
            total+=1
    f.close()
    print match + "/" + total


def processByScoreId(scoreid):
    url = endpoint  + '/' + str(scoreid) + '.' +format + '&oauth_consumer_key=' + apikey
    r = requests.get(url)
    score = r.json()
    processScore(score)




#processPages("All about that bass")
processPages()
# processByScoreId(413861) # japanese, no crash
#processByScoreId(508521)
#processByScoreId(507126) # should bring nothing
#processByScoreId(506671) # it's raining men - The wearther girls
#processByScoreId(508456) # Bohemian Rapsody - Queen
 
                
