from apiwrappers.spotify import create_spotify_track
from apiwrappers.musicdatatype import MusicDataType
from dtwmatcher.dtwmatch import normalize
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from dtwmatcher.dtwmatch import *
from apiwrappers.musescore import *
s= create_score('410')
cand_id = "6Odmkrg0zhn49cW8VZWGGr"
cand_id_2 = "3GzfPCdN3Gc7q2u5cIoYTP"
cand = create_spotify_track(cand_id)
cand_chro = cand.get_chromagram(MusicDataType.ECHONEST)
cand_2 = create_spotify_track(cand_id_2)
cand_2_chro = cand_2.get_chromagram(MusicDataType.ECHONEST)

reference = s.get_chromagram(MusicDataType.AUDIO)

plt.subplot(1, 3, 1)
plt.imshow(reference.T,  aspect='auto')
plt.subplot(1, 3, 2)
plt.imshow(cand_chro.T,   aspect='auto')
plt.subplot(1,3, 3)
plt.imshow(cand_2_chro.T,   aspect='auto')
plt.show()

print rdtw_global_match_score(reference,cand_2_chro)
print rdtw_global_match_score(reference,cand_chro)
# print rdtw_global_match_score(reference,cand.get_chromagram(MusicDataType.ECHONEST))
# print rdtw_global_match_score(reference,cand_2.get_chromagram(MusicDataType.ECHONEST))
        # for j,e in enumerate(el):
        #     if el<0.2
        #         e[j]=0