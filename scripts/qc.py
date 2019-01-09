
import os
from os.path import join
import numpy as np
import util
import pickle
import matplotlib.pyplot as plt
from matplotlib import pylab
from pprint import pprint

def get_elementlist_from_matlist(mat_list):
    mean, std_dev = util.findMeanAndStd(mat_list)
    np.fill_diagonal(std_dev, 1)
    normalized_mat_list = []
    for mat in mat_list:
        assert (mat.shape == mean.shape) and (
                    mat.shape == std_dev.shape), "Shape Mismatch between mean, stddev or matrixt"
        normalized_mat_list.append(abs(mat - mean) / std_dev)
    element_list = np.array(util.groupElementsOfMatrices(normalized_mat_list))
    return element_list


def qc1(mat_list, expected_outlier_percent):
    element_list = get_elementlist_from_matlist(mat_list)
    nCon, nSub = element_list.shape
    outlier_connections = element_list > 2
    outlier_connections = (outlier_connections.sum(axis=0) / nCon) > expected_outlier_percent
    count = outlier_connections.sum()

    return count


def qc2(mat_list, expected_outlier_percent):
    element_list = get_elementlist_from_matlist(mat_list)
    avg = element_list.mean(axis=1)

    threshold_factor = 4
    nCon, nSub = element_list.shape

    count = 0
    for i in range(0, nSub):
        outlier_connections = (element_list[:, i] - threshold_factor * avg > 0)
        percent_outlier = outlier_connections.sum() / nCon
        if percent_outlier > expected_outlier_percent:
            count = count + 1

    return count


def qc3(mat_list, expected_outlier_percent):
    threshold = 0.02

    mean, std_dev = util.findMeanAndStd(mat_list)
    mean = mean > threshold
    dim = len(mat_list[0])
    expected_outlier = expected_outlier_percent * dim * dim # % of the connections
    count = 0
    for i in range(0, len(mat_list)):
        nOutlier = ((mat_list[i] > threshold) != mean).sum()

        if nOutlier > expected_outlier:
            count = count + 1

    return count

def qc4(mat_list, expected_outlier_percent):
    dim = len(mat_list[0])
    threshold = 0.3
    distances = []
    for i in range(0, len(mat_list)):
        d = []
        for j in range(0, len(mat_list)):
            if i != j:
                d.append(((mat_list[i] > threshold) != (mat_list[j] > threshold)).sum())
        distances.append(np.percentile(d, 0.5))

    return (np.asarray(distances) > expected_outlier_percent * dim * dim).sum()
if __name__ == '__main__':
    directory = 'AD-Data'
    mat_list = util.readMatricesFromDirectory(join(os.pardir, directory))
    threshold = [i/10 for i in range(0, 10)]

    try:
        qc1_outlier_count = pickle.load(open('qc1_outlier_count.p', 'rb'))
    except FileNotFoundError:
        qc1_outlier_count = []
        for t in threshold:
            qc1_outlier_count.append(qc1(mat_list, t))
        pickle.dump(qc1_outlier_count, open('qc1_outlier_count.p', 'wb'))

    try:
        qc2_outlier_count = pickle.load(open('qc2_outlier_count.p', 'rb'))
    except FileNotFoundError:
        qc2_outlier_count = []
        for t in threshold:
            qc2_outlier_count.append(qc2(mat_list, t))
        pickle.dump(qc2_outlier_count, open('qc2_outlier_count.p', 'wb'))

    try:
        qc3_outlier_count = pickle.load(open('qc3_outlier_count.p', 'rb'))
    except FileNotFoundError:
        qc3_outlier_count = []
        for t in threshold:
            qc3_outlier_count.append(qc3(mat_list, t))
        pickle.dump(qc3_outlier_count, open('qc3_outlier_count.p', 'wb'))

    try:
        qc4_outlier_count = pickle.load(open('qc4_outlier_count.p', 'rb'))
    except FileNotFoundError:
        qc4_outlier_count = []
        for t in threshold:
            qc4_outlier_count.append(qc4(mat_list, t))
        pickle.dump(qc1_outlier_count, open('qc4_outlier_count.p', 'wb'))

    print("Done !!!")
    plt.subplot(2, 2, 1)
    plt.title("QC1")
    plt.xlabel("outlier percentage")
    plt.ylabel("number of outlier")
    plt.subplots_adjust(bottom=0.5)
    plt.plot(threshold, qc1_outlier_count)
    plt.subplot(2, 2, 2)
    plt.title("QC2")
    plt.xlabel("outlier percentage")
    plt.ylabel("number of outlier")
    plt.subplots_adjust(bottom=0.5)
    plt.plot(threshold, qc2_outlier_count)
    plt.subplot(2, 2, 3)
    plt.title("QC3")
    plt.xlabel("outlier percentage")
    plt.ylabel("number of outlier")
    plt.plot(threshold, qc3_outlier_count)
    plt.subplot(2, 2, 4)
    plt.title("QC4")
    plt.xlabel("outlier percentage")
    plt.ylabel("number of outlier")
    plt.plot(threshold, qc4_outlier_count)

    pylab.savefig('qc.png')
    plt.show()





