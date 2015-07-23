#!/usr/bin/python
# -*- coding: utf-8 -*-

from dtw import dtw
import rpy2.robjects.numpy2ri
from rpy2.robjects.packages import importr
rpy2.robjects.numpy2ri.activate()
import rpy2.robjects as ro
R = rpy2.robjects.r
DTW = importr('dtw')


def l2norm(x, y):
    return x * x + y * y


def dtw_global_match_score(template, query):
    (dist, cost, path) = dtw(query, template, l2norm)
    pathLength = len(path[0])
    return dist / pathLength


def rdtw_subsequence_match_score(template, query):

    alignment = R.dtw(query, template, open_begin=True, open_end=True,
                      step_pattern=R('asymmetric'))
    return alignment.rx('normalizedDistance')[0][0]


def rdtw_global_match_score(template, query):
    alignment = R.dtw(query, template, keep=False,
                      keep_internals=False, distance_only=True)
    return alignment.rx('normalizedDistance')[0][0]


def fastdtw_global_match_score(template, query):
    (distance, path) = fastdtw(query, template, dist=lambda a, b: \
                               np.linalg.norm(a - b))
    return distance / len(path)
