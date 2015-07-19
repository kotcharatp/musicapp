__author__ = 'hibiki'

import csv
import platform
import io
import subprocess
import numpy
from scipy.io.wavfile import read


def extract_frequency(audio_fname, out_fname):

    # a list containing tuples of (time, freq)
    time_freq = []

    # load correct binary of sonic annotator
    if platform.system() == 'Darwin':
        sonic_path = 'bin/sonic-annotator_osx'
    elif platform.system() == 'Linux':
        sonic_path = 'bin/sonic-annotator_linux'

    # pass to sonic annotator for pitch extraction
    pitch_output = subprocess.check_output([sonic_path, '-d', 'vamp:pyin:pyin:smoothedpitchtrack',
                                            audio_fname, '-w', 'csv', '--csv-stdout'])
    pitch_output = io.StringIO(pitch_output.decode(encoding='UTF-8'))

    # extract csv into time and freq
    reader = csv.reader(pitch_output, delimiter=',')
    for row in reader:
        time_freq.append((row[1], row[2]))

    # write to output file
    with open(out_fname, 'w') as out:
        for (t, f) in time_freq:
            out.write(t + ',' + f + '\n')


def extract_amplitude(audio_fname, out_fname):
    # read audio file
    samprate, wavdata = read(audio_fname)
    # write to output file
    i = 0
    with open(out_fname, 'w') as out:
        for value in wavdata:
            # handle 2 channel audio
            if not isinstance(value, numpy.int16):
                value = (value[0] + value[1]) / 2
            out.write(str(i) + ',' + str(value) + '\n')
            i += 1


def extract_duration():
    # read freq.csv and extract last time component
    with open('share/freq.csv') as freq_data:
        reader = csv.reader(freq_data, delimiter=',')
        records = [row for row in reader]
        return records[len(records)-1][0]


