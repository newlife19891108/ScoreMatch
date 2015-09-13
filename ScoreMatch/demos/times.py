import numpy as np
from dtwmatcher.dtwmatch import *
import timeit
def f():
	cand = np.loadtxt("1KBEjHfFUtonyNbEPV6Ux5.csv")
	temp = np.loadtxt("114295.csv")
	rdtw_global_match_score(temp,cand)
cand = np.loadtxt("3GwwzKCUwZQyhZ1WQm9AeO.csv")
temp = np.loadtxt("114295.csv")
num_of_frames = cand.shape[0]*temp.shape[0]
num_of_seconds = 354*311
print num_of_frames
print num_of_seconds
print 10.353126049*((180*180.0)/num_of_seconds*1.0)
cand_2 = np.loadtxt("4rYk0SjHmHPYk9WxEklojF.csv")

cand_3 = np.loadtxt("3GwwzKCUwZQyhZ1WQm9AeO.csv")
t = timeit.Timer("f()","from __main__ import f")
secs =  t.timeit(number=1)
print secs
print secs * ((180*180)/num_of_seconds*1.0)
# rdtw_global_match_score(temp,cand_2)
# rdtw_global_match_score(temp,cand_3)
