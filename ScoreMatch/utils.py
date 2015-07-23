#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import mido as md
import matplotlib.pyplot as plt
import urllib
import os
import subprocess
import sys


def get_chromagram_from_audio(file_name, csv_out=''):
    command = 'sonic-annotator -t hpcp.n3 ' + file_name \
        + ' -w csv --csv-stdout'

    # os.system()

    result = subprocess.check_output(command, shell=True)
    first_comma = result.find(',')

    array = np.fromstring(result[first_comma + 1:], sep=',')
    columns = 13
    rows = len(array) / columns
    out = np.reshape(array, (rows, columns))
    if csv_out != '':
        np.savetxt(csv_out, out, delimiter=',', fmt='%.9f')
    return out[:, 1:]


def get_chromagram_from_midi(file_name, csv_out=''):
    mid = md.MidiFile(file_name)
    times = np.array([m.time for m in mid])

    offsets = np.cumsum(times)
    register = [0] * 128
    matrix_register = []

    for (message, time) in zip(mid, offsets):
        if not isinstance(message, md.MetaMessage) and message.type \
            == 'note_on':
            note = message.note
            if message.velocity == 0:
                beg = register[note][1]
                end = time
                matrix_register.append((note, beg, end))
            else:
                register[note] = (note, time)
    windowSize = 4096 * 4
    windowTime = windowSize / 48000.0
    matrixlen = int(round(matrix_register[-1][2] / windowTime))
    chromamatrix = [[0] * 12] * matrixlen
    chromamatrix = np.array(chromamatrix, dtype=np.dtype('b'))
    for el in matrix_register:
        note = el[0]
        octave = (note + 3) % 12
        beg = int(round(el[1] / windowTime))

        end = int(round(el[2] / windowTime))
        if beg == end:
            end = end + 1
        chromamatrix[beg:end, octave] = 1
    times = np.arange(0, matrixlen) * windowTime
    times = times.reshape((matrixlen, 1))
    chromagram = np.hstack((times, chromamatrix))

    if csv_out != '':
        np.savetxt(csv_out, chromagram, delimiter=',', fmt='%.3f')

    return chromamatrix


def get_chromagram_from_csv(path):
    arr = np.loadtxt(path, delimiter=',')
    chromagram = arr[:, 1:]
    return chromagram


def download_file(link, target):
    urllib.urlretrieve(link, target)


def remove_file(path):
    os.system('rm ' + path)
