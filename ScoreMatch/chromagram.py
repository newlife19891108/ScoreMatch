import librosa
import wave
def getChromagram(path):
	y, fs = librosa.load	(path)
	return librosa.feature.chroma_stft(y=y, fs=fs)


getChromagram('./audio_samples/melody7.wav')