import dtwMatch
import chromagram

chroma_seq_1=getChromagram('./audio_samples/melody7.wav')
chroma_seq_2=getChromagram('./audio_samples/melody8.wav')
chroma_seq_3=getChromagram('./audio_samples/melody14.wav')

target=chroma_seq_1
candidates=[chroma_seq_3,chroma_seq_2]
scores=[]
for candidate in candidates:
	score=dtwGlobalMatchScore(target,candidate)
	scores.append(score)