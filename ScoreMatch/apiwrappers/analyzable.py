#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc


class Analyzable(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, id):
        self.id = id

    @abc.abstractmethod
    def get_chromagram():
        return
    @abc.abstractmethod
    def get_echonest_analysis():
        return