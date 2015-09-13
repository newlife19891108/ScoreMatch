#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import string
socket.setdefaulttimeout(90)
import numpy as np
import mido as md
import matplotlib.pyplot as plt
import urllib
import os
import subprocess
import sys
import config
import re
from subprocess import Popen, PIPE

def num_common_words(string1, string2):
    string1 = normalize(string1)
    string2 = normalize(string2)
    list1 = string1.split()
    list2 = string2.split()

    common = set(list1).intersection(set(list2))
    return len(common)
def remove_multi_spaces_from_text(text):
    """ Lorem    ipsum  dolar  -> Lorem Ipsum Dolar
    """
    return ' '.join(text.split())

def get_chromagram_from_audio(file_name, csv_out=''):
    """Creates a chromagram from the local audio using local vamp chroma extractors

        Args:
            file_name: path for the audio
            csv_out: records the chroma extractor in this path if given

        Returns:
            Chromagram for the audio
    """
    command = 'sonic-annotator -t hpcp.n3 ' + file_name \
        + ' -w csv --csv-stdout'

    # os.system()
    FNULL = open(os.devnull, 'w')
    #p = Popen(['sonic-annotator','-t', 'chroma.n3',file_name,'--csv-stdout'],stdin=PIPE, stdout=PIPE, stderr=PIPE)
    #p = Popen(['sonic-annotator','-t', 'chroma.n3',file_name],stdin=PIPE, stdout=PIPE, stderr=PIPE)

    #result, err = p.communicate(b"input data that is passed to subprocess' stdin")
    try:
        result = subprocess.check_output(command,stderr=FNULL,shell=True)
    except subprocess.CalledProcessError,e :
        raise ValueError('A very specific bad thing happened')

    first_comma = result.find(',')
    array = np.fromstring(result[first_comma + 1:], sep=',')
    columns = 13
    rows = len(array) / columns
    out = np.reshape(array, (rows, columns))
    if csv_out != '':
        np.savetxt(csv_out, out, delimiter=',', fmt='%.9f')
    return out[:, 1:]
def normalize(s):
    out = s.lower()
    return re.sub('[%s]' % re.escape(string.punctuation), '', out)

def derive_window_size_from_midi(file_name):
    """Finds best window size for quantizing the midi while creating chromagram from the midi.
    Minimum duration of all the midi note events are found.The midi should not be quantized higher than this duration not to lose information.

    Args:
        file_name: path for the midi file
    Returns:
        Minimum note duration
    """
    mid = md.MidiFile(file_name)
    times = np.array([m.time for m in mid])

    offsets = np.cumsum(times)
    register = [0] * 128
    matrix_register = []
    min_dur = 1500
    min_on = 100
    max_on = 0
    for (message, time) in zip(mid, offsets):
        print message,time
        if not isinstance(message, md.MetaMessage) and message.type \
            == 'note_on':
            note = message.note
            if message.velocity == 0:
                beg = register[note][1]
                end = time
                matrix_register.append((note, beg, end))

                min_dur = min(min_dur,end-beg)
                max_on = max(end,max_on)
            else:
                min_on =min(min_on,time)
                register[note] = (note, time)
    print min_on,max_on,min_dur
    return min_dur

def get_chromagram_from_midi(file_name, csv_out=''):
    """Creates a chromagram from the local midi.

    This calculates an artificial chromagram . The midi is quantized into time units. Then for each time unit a vector representing all note classes are created
    and the note classes that are active on that time unit are marked with 1 on the vector. Others left 0.


        Args:
            file_name: path for the audio
            csv_out: records the chroma extractor in this path if given

        Returns:
            Chromagram for the audio
    """
    print "filename",file_name
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
    window_size = config.window_size
    window_time = config.window_time
    matrixlen = int(round(matrix_register[-1][2] / window_time))
    chromamatrix = [[0] * 12] * matrixlen
    chromamatrix = np.array(chromamatrix, dtype=np.dtype('b'))
    for el in matrix_register:
        note = el[0]
        octave = (note + 3) % 12
        beg = int(round(el[1] / window_time))

        end = int(round(el[2] / window_time))
        if beg == end:
            end = end + 1
        chromamatrix[beg:end, octave] = 1
    times = np.arange(0, matrixlen) * window_time
    times = times.reshape((matrixlen, 1))
    chromagram = np.hstack((times, chromamatrix))

    if csv_out != '':
        np.savetxt(csv_out, chromagram, delimiter=',', fmt='%.3f')

    return chromamatrix


def get_chromagram_from_csv(path):
    """
        Reads chromagram from a csv file
    """
    arr = read_csv(path)
    chromagram = arr[:, 1:]
    return chromagram
def read_csv(path):
    return np.loadtxt(path,delimiter=',')
def read_lines_from_file(path):
    with open(path) as f:
        lines = f.readlines()
    return lines
def download_file(link, target):
    while True:
        try:
            urllib.urlretrieve(link, target)
            print "file downloaded from ",link  
            break
        except socket.timeout:
            continue


def remove_file(path):
    os.system('rm ' + path)

def filter_text(text):

    """Filter the text by removing some stopwords and some specific tokens:

        | text in parenthesis
        | years
        | stopwords and,or not,by,arranged,music,lyris,arr.,arr,mus, and notated

    BWV 847 arr. by Andres Segovia (1945) (some repetitions are removed from the score) -> BWV 847 Andres Segovia

    """
        #query = query.translate(string.maketrans("",""), string.punctuation)
    text = re.sub('\(.*\)', '', text)
    text = re.sub('\d{4}','',text)
    text = text.replace('|', ' ')
    stop = set((('and', 'or', 'not','by','arranged','music','lyrics','arr.','arr','mus','notated')))
    text = " ".join([word for word in text.split() if word.lower() not in stop])
    return text

def token_match(target_text,check_text):
    if check_text=="" or target_text=="":
        return False;
    target_tokens = target_text.split()
    check_set = set(check_text.split())
    for t in target_tokens:
        if t not in check_set:
            return False
    return True
def token_remove(target_text,check_text):
    if check_text=="" or target_text=="":
        return false;
    target_tokens = target_text.split()
    check_tokens = check_text.split()
    for t in target_tokens:
        if t in check_tokens:
            check_tokens.remove(t)
    return " ".join(check_tokens)
