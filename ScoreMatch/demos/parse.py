import numpy as np
from apiwrappers.musescore import *
import apiwrappers.track
from apiwrappers.spotify import *

import time
data =  np.loadtxt('resultsx.csv',delimiter=',',dtype=np.dtype(str))
f = open('resultcomplete.csv','w')
for el in data:
	if el[2]!="nomatch":
		if el[-2]=='spotify':
			time.sleep(3)
			uri = get_spotify_uri_by_id(el[2])
			el = np.append(el,uri)
		else: 
			el = np.append(el,uri)
	else:
		print "nomatch"
z3	f.write(",".join(el))
	f.write("\n")
f.close()