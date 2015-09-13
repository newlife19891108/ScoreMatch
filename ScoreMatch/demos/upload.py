import os
audios = [each for each in os.listdir('../out4') if each.endswith('.mp3')]
import time
import apiwrappers.echonest as echonest
i = 0
for audio in audios:
	
	#data,file_exists = echonest.check_file_exists('../out5/'+audio)
	print echonest.get_echonest_track_for_file('../out4/'+audio)
	# print data
	# if not file_exists:
	# 	print audio,"not yet"
	# 	print data
	time.sleep(4)
	i = i+1
	print i 