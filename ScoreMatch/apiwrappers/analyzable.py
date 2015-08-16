#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc


class Analyzable(object):

    """This is an abstracted class for other audio related instances.

    The subclasses of this have to have a function which returns a chromagram.

    Attributes:
        id: id of the analyzable.Can be spotify,echonest or musescore id depending on the subclass inheriting it.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, id):
        self.id = id

    @abc.abstractmethod
    def get_chromagram():
        """This function has to return a chromagram. This is what characterizes analyzable

        """        
        return
