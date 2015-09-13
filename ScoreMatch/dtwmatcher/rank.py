#!/usr/bin/python
# -*- coding: utf-8 -*-

from dtwmatcher.dtwmatch import *
from apiwrappers.musicdatatype import MusicDataType


def rank(
    reference,
    candidates,
    chroma_function,
    dtw_function,
    ):

    template = chroma_function(reference)
    score_list = []
    for candidate in candidates:
        score_list.append((candidate, dtw_function(template,
                          chroma_function(candidate))))
    return sorted(score_list, key=lambda candidate: candidate[1])


def rank_analyzables(reference, candidates, mode='partial'):
    """
        Ranks list of :class:`.Analyzable` candidates with respect to a single reference `.Analyzable` based on their chromagrams

        Matching scores can be calculated between for each candidate and the reference.Then the candidate list is sorted in increasing order(best matching to worst matching)
        Analyzable can be :class:`apiwrappers.spotifytrack.SpotifyTrack`, :class:`apiwrappers.score.Score` or :class:`apiwrappers.echonestsong.EchonestSong`

        Args:
            reference: Reference :class:`.Analyzable`

            candidates: List of `.Analyzable` that will be ranked

            mode: 'partial' or 'full'. If partial matching calculated based on subsequence matching :meth:`dtwmatcher.dtwmatch.rdtw_subsequence_match_score`

            otherwise based on full length sequence matching :meth:`dtwmatcher.dtwmatch.rdtw_global_match_score`
            
        Returns:
            List of ranked candidates with respect to audio matching scores

    """

    sorted_list = []
    if mode == 'partial':
        dtw_function = rdtw_subsequence_match_score
        template = reference.get_chromagram(MusicDataType.AUDIO)
    elif mode == 'full':

        dtw_function = rdtw_global_match_score
        print 'chroma for score'
        template = reference.get_chromagram(MusicDataType.ECHONEST)
        print 'chroma for score complete'
    if mode == 'partial':
        for candidate in candidates:
            sorted_list.append((candidate, dtw_function(template,
                               candidate.get_chromagram(MusicDataType.AUDIO))))
    elif mode == 'full':
        for candidate in candidates:
            print 'waiting chromagram for candidate'
            candidate_chroma = \
                candidate.get_chromagram(MusicDataType.ECHONEST)
            print 'chroma taken for candidate'
            if candidate_chroma != None:
                sorted_list.append((candidate, dtw_function(template,
                                   candidate_chroma)))
    sorted_list.sort(key=lambda candidate: candidate[1])
    return sorted_list
