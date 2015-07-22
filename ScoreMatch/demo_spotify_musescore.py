from  musescore import *
from  spotify import *

from Track import *
from score import *
import os
from midi2chroma import *
from rank import *
from chromagram import *
from dtwMatch import *

query = getSearchQueryForScore("114295")
tracks = querySpotify(query)
s = createScore("114295")
midi_name =s.id+".mid"
template = s.id+".csv"
urllib.urlretrieve(s.midi,s.id+".mid")
getChroma(midi_name,template)
candidates = []
for track in tracks:
	file_name = track.id+".mp3"
	urllib.urlretrieve(track.preview_url,track.id+".mp3")
	os.system("sonic-annotator -t hpcp.n3 " + file_name + " -w csv --csv-force")
	csv_name = track.id + "_vamp_vamp-hpcp-mtg_MTG-HPCP_HPCP.csv"
	candidates.append(csv_name)
print rank(template,candidates,getChromagramFromCSV,rdtwSubsequenceMatchScore)
for track in tracks:
	print track.id,track.name