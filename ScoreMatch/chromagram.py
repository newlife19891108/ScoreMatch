import librosa
import wave
import numpy as np
def getChromagramLibrosa(path):
	y, fs = librosa.load	(path)
	return librosa.feature.chroma_stft(y=y, fs=fs)
def getChromagramFromCSV(path):
	arr=np.loadtxt(path,delimiter=",")
	chromagram=arr[:,1:]
	return chromagram


