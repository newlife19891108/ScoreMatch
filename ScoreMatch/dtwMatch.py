from dtw import dtw
def l2norm(x,y):
	return (x * x) + (y * y)

def dtwGlobalMatchScore(sequence1,sequence2):
	return 5;
	# dist, cost, path = dtw(sequence1, sequence2, l2norm)
	# pathLength = len(path[0])
	# return dist/pathLength

#def dftSubsequenceMatchScore(sequence1,sequence2):