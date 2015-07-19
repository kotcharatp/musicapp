__author__ = 'hibiki'

import csv
import json
import numpy as np


# Gaussian Smooth
def smooth_list_gaussian(list_of_values, degree=5):

    if degree == 0:
        return list_of_values

    window = degree*2-1
    weight = np.array([1.0]*window)
    weight_gauss = []

    for i in range(window):
        i = i-degree+1
        frac = i/float(window)
        gauss = 1/(np.exp((4*(frac))**2))
        weight_gauss.append(gauss)

    weight = np.array(weight_gauss)*weight
    smoothed = [0.0]*(len(list_of_values)-window)

    for i in range(len(smoothed)):
        smoothed[i] = sum(np.array(list_of_values[i:i+window])*weight)/sum(weight)

    return smoothed


# load pitch and amplitude then sampling it to the same size, to be ready for plotting or gauss
# the function returns the array of (time, amp, freq)
def prepare(pitch, amp):

    # load Pitch and amplitude csv as pitch_array and amp_array
    with open(pitch, 'r') as dest_f:
        data_iter = csv.reader(dest_f, delimiter=',', quotechar='"')
        data = [data for data in data_iter]
    pitch_array = np.asarray(data, dtype=np.float64)

    with open(amp, 'r') as dest_f:
        data_iter = csv.reader(dest_f, delimiter=',', quotechar='"')
        data = [data for data in data_iter]
    amp_array = np.asarray(data, dtype=np.float64)

    # create the list of pitch and amplitude from what we got
    ys_p = pitch_array[:, 1]
    xs_p = np.arange(1, len(ys_p)+1, 1)     # allocate time sampling

    xs_a = amp_array[:, 0]
    ys_a = amp_array[:, 1]

    # just to absolute the amplitude because it can be negative
    ys_a = list(map(abs, ys_a))

    # compute the blocksize to be used in mapping amplitude
    bs = float(len(ys_a))/len(ys_p)

    new_amp_in_pitch = []
    old_i = 0

    # cut into block size, compute mean, append into list
    for i in range (int(round(bs)), len(ys_a), int(round(bs))):
        m = np.mean(ys_a[old_i:i])
        new_amp_in_pitch.append(m)
        old_i = i

    # just to pad the amplitude
    # in case we get error from down sampling
    diff = abs(len(xs_p)-len(new_amp_in_pitch))
    for i in range(diff):
        new_amp_in_pitch.append(0)

    # save in time, freq, amp
    all_values = np.zeros((len(xs_p), 3))
    all_values[:, 0] = xs_p
    all_values[:, 1] = ys_p
    all_values[:, 2] = new_amp_in_pitch[:len(xs_p)]

    return all_values


# Smooth amplitude, Pitch  and then packed in y_ag, y_pg ( Y_AmplitudeGaussian, Y_PitchGaussian )
# we might not get the same amount of amplitude(graph may shift).
# In this case I do zero padding in front of the list, so we can get graph almost the same as the original
def smooth(all_values, degree_freq, degree_amp):
    time = all_values[:, 0]
    freq = all_values[:, 1]
    amp = all_values[:, 2]

    smooth_freq = smooth_list_gaussian(freq, degree_freq)
    mean_of_sf = np.mean(smooth_freq)
    freq_gauss = np.zeros(len(time))
    freq_gauss[:len(time)-len(smooth_freq)] = mean_of_sf
    freq_gauss[len(time)-len(smooth_freq):] = smooth_freq

    smooth_amp = smooth_list_gaussian(amp, degree_amp)
    amp_gauss = np.zeros(len(time))
    amp_gauss[:len(time)-len(smooth_amp)] = 0
    amp_gauss[len(time)-len(smooth_amp):] = smooth_amp

    all_values = np.zeros((len(time), 3))
    all_values[:, 0] = time
    all_values[:, 1] = freq_gauss
    all_values[:, 2] = amp_gauss

    return all_values


# all gaussianed export json data in field of (t(time),f(freq),a(amplitute))
def export(all_values):

    with open('all.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(all_values)

    csv_file = open('all.csv', 'r')
    json_file = open('www-source/dataset.js', 'w')

    fieldnames = ("t", "f", "a")
    reader = csv.DictReader(csv_file, fieldnames)

    # just to create item dataset, so it is easier to use with js
    data = json.dumps([r for r in reader])
    json_file.write("var dataset = ")
    json_file.write(data)
