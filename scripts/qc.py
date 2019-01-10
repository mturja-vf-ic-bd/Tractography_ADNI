
import os
from os.path import join
import numpy as np
import util
import pickle
import matplotlib.pyplot as plt
from matplotlib import pylab
from pprint import pprint

mean_total_connections = 5000

def find_outlier(list):
    list = np.asarray(list)
    list_std = np.std(list)
    list_mean = np.mean(list)
    list = abs(list - list_mean)/list_std > 3
    return list

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


def qc1(mat_list):
    element_list = get_elementlist_from_matlist(mat_list)
    outlier_connections = element_list > 2
    outlier_connections = outlier_connections.sum(axis=0)
    count = find_outlier(outlier_connections).sum()

    return count


def qc2(mat_list):
    element_list = get_elementlist_from_matlist(mat_list)
    avg = element_list.mean(axis=1)

    threshold_factor = 3
    nCon, nSub = element_list.shape

    outlier_count = []
    for i in range(0, nSub):
        outlier_connections = (element_list[:, i] - threshold_factor * avg > 0)
        outlier_count.append(outlier_connections.sum())

    return find_outlier(outlier_count).sum()


def qc3(mat_list, threshold):
    mean, std_dev = util.findMeanAndStd(mat_list)
    mean = mean > threshold
    outlier_count = []
    for i in range(0, len(mat_list)):
        nOutlier = ((mat_list[i] > threshold) != mean).sum()
        outlier_count.append(nOutlier)

    return find_outlier(outlier_count).sum()

def qc4(mat_list, threshold):
    distances = []
    for i in range(0, len(mat_list)):
        d = []
        for j in range(0, len(mat_list)):
            if i != j:
                d.append(((mat_list[i] > threshold) != (mat_list[j] > threshold)).sum())
        distances.append(np.percentile(d, 0.5))

    return find_outlier(distances).sum()


if __name__ == '__main__':
    directory = 'AD-Data'
    mat_list = util.readMatricesFromDirectory(join(os.pardir, directory))
    '''
    print('QC1 Outlier Count : ',
          qc1(mat_list))
    print('QC2 Outlier Count : ',
          qc2(mat_list))
    print('QC3 Outlier Count : ',
          qc3(mat_list))
    print('QC4 Outlier Count : ',
          qc4(mat_list))
          '''

    t = [i/20 for i in range(0, 20)]
    try:
        qc3_outlier = pickle.load(open('qc3_outlier.p', 'rb'))
        qc4_outlier = pickle.load(open('qc4_outlier.p', 'rb'))
    except:
        qc3_outlier = []
        qc4_outlier = []
        for i in t:
            qc3_outlier.append(qc3(mat_list, i))
            qc4_outlier.append(qc4(mat_list, i))

    pickle.dump(qc3_outlier, open('qc3_outlier.p', 'wb'))
    pickle.dump(qc4_outlier, open('qc4_outlier.p', 'wb'))
    print("Done !!!")

    plt.subplot(1, 2, 1)
    plt.title("QC3")
    plt.xlabel("threshold")
    plt.ylabel("number of outlier")
    plt.plot(t, qc3_outlier)
    plt.subplot(1, 2, 2)
    plt.title("QC4")
    plt.xlabel("threshold")
    plt.ylabel("number of outlier")
    plt.plot(t, qc4_outlier)
    pylab.savefig('qc.png')
    plt.show()
    '''
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
    '''





