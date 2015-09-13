#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.cm as cm
import rpy2.robjects.numpy2ri
from rpy2.robjects.packages import importr
rpy2.robjects.numpy2ri.activate()
import rpy2.robjects as ro
import rpy2.rinterface as sikik
R = rpy2.robjects.r
DTW = importr('dtw')
from matplotlib import pyplot as plt
import math
import sys
def rdtw_subsequence_match_score(template, query):
    """Finds a cost of subsequence matching for shorter sequence in a longer sequence
    
     Args:
        template:timeseries(single or multidimensional np.array) in which subsequence time series will be found

        query:subsequence timeseries(single or multidimensional np.array) that will be searched in template

    Returns:
        A float cost for the existence of query in the template
    """

    alignment = R.dtw(
        query,
        template,
        open_begin=True,
        open_end=True,
        keep_internals=True,
        step_pattern=R('symmetricP1'),
        )

    # print len(query), len(template)
    # R.plot(alignment,type="density")
    # print alignment.rx('index1')
    # print alignment.rx('index2')
    # raw_input("wait")

    print alignment.rx('distance')[0][0], \
        alignment.rx('normalizedDistance')[0][0]
    return alignment.rx('distance')[0][0]

def rdtw_global_match_score(template, query):
    """Finds a cost of matching given a two time series

    Args:
        template:Timeseries(multi or singledimensional np.array) in which subsequence time series will be found

        query:Timeseries(multi or singledimensional np.array) that will be searched in template

    Returns:
        A float cost for the amount of matching

    """

    print 'dtw calculating'
    try:

        alignment = R.dtw(query, template,
                dist_method='cosine')

        #R.plot(alignment,type="density")
        # plt.subplot(1, 2, 1)
        # plt.imshow(template.T,  aspect='auto')
        # plt.subplot(1, 2, 2)
        # plt.imshow(query.T,   aspect='auto')
        # plt.show()
        # print alignment.rx('costMatrix')[0][0]
        # print alignment.rx('distance')[0][0], \
        #     alignment.rx('normalizedDistance')[0][0], len(template), \
        #     len(query)
    except sikik.RRuntimeError, e:

        print 'no alignment'
        return 10000000
    x = len(query)
    y = len(template)


    print 'dtw calculated'
    division_fact = math.sqrt(len(template)*len(template)+len(query)*len(query))
    division_fact = len(alignment.rx('index1')[0])
    #print len(alignment.rx('index1')[0]),len(alignment.rx('index2')[0])
    return alignment.rx('distance')[0][0]/division_fact,alignment.rx('index2')[0][0],alignment.rx('index2')[0][-1]
