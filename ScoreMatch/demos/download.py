import utils
import socket

socket.setdefaulttimeout(1)
try:
	utils.download_file('https://musescore.com/score/1129926/download/mp3','asf.mp3')
except Exception,e:
  print type(e)