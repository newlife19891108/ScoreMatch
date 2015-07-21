from dtw import dtw
from fastdtw import *
import rpy2.robjects.numpy2ri
from rpy2.robjects.packages import importr
rpy2.robjects.numpy2ri.activate()
import rpy2.robjects as ro
R = rpy2.robjects.r
DTW = importr('dtw')
def l2norm(x,y):
	return (x * x) + (y * y)
def dtwGlobalMatchScore(template,query):
	dist, cost, path = dtw(query, template, l2norm)
	pathLength = len(path[0])
	return dist/pathLength
def rdtwSubsequenceMatchScore(template,query):

	alignment = R.dtw(query, template, 
                 open_begin=True, open_end=True,
                 step_pattern=R('asymmetric')
                 )
	return alignment.rx('normalizedDistance')[0][0]
def rdtwGlobalMatchScore(template,query):
	alignment = R.dtw(query, template,keep=False,keep_internals=False,distance_only=True)
	return alignment.rx('normalizedDistance')[0][0]

def fastdtwGlobalMatchScore(template,query):
	(distance,path,) = fastdtw(query,template,dist=lambda a, b: np.linalg.norm(a-b))
	return distance/len(path)