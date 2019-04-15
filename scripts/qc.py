
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
                    mat.shape == std_dev.shape), "Shape Mismatch between mean, stddev or matrix"
        normalized_mat_list.append(abs(mat - mean) / std_dev)
    element_list = np.array(util.groupElementsOfMatrices(normalized_mat_list))
    return element_list

def threshold_matrix(mat_list, threshold):
    for i in range(0, len(mat_list)):
        matrix = np.asarray(mat_list[i])
        mat_list[i] = (matrix > threshold) * matrix

    return mat_list

def qc1(mat_list, threshold):
    mat_list = threshold_matrix(mat_list, threshold)
    element_list = get_elementlist_from_matlist(mat_list)
    outlier_connections = element_list > 2
    outlier_connections = outlier_connections.sum(axis=0)
    count = find_outlier(outlier_connections).sum()

    return count


def qc2(mat_list, threshold):
    mat_list = threshold_matrix(mat_list, threshold)
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

    outlier_I = find_outlier(outlier_count)
    return outlier_I.sum(), outlier_I


def qc4(mat_list, threshold):
    distances = []
    for i in range(0, len(mat_list)):
        d = []
        for j in range(0, len(mat_list)):
            if i != j:
                d.append(((mat_list[i] > threshold) != (mat_list[j] > threshold)).sum())
        distances.append(np.percentile(d, 0.3))

    outlier_I = find_outlier(distances)
    return outlier_I.sum(), outlier_I


if __name__ == '__main__':
    directory = '/home/turja/AD-Data'
    mat_list, fnames = util.readMatricesFromDirectory(join(os.pardir, directory), False)
    #threshold = [i/20 for i in range(0, 20)]
    threshold = [0.001, 0.002, 0.005]
    enforce = 1
    if enforce == 0:
        #qc1_outlier = pickle.load(open('qc1_outlier.p', 'rb'))
        #qc2_outlier = pickle.load(open('qc2_outlier.p', 'rb'))
        qc3_outlier = pickle.load(open('qc3_outlier.p', 'rb'))
        qc4_outlier = pickle.load(open('qc4_outlier.p', 'rb'))
    else:
        qc1_outlier = []
        qc2_outlier = []
        qc3_outlier = []
        qc4_outlier = []
        for i in threshold:
            print("Threshold : ", i)
            #qc1_outlier.append(qc1(mat_list, i))
            #qc2_outlier.append(qc2(mat_list, i))
            qc3_c, qc3_i = qc3(mat_list, i)
            qc3_outlier.append(qc3_c)
            print("QC3 Count: ", qc3_c)
            for t in range(0, len(fnames)):
                if qc3_i[t] == 1:
                    print(fnames[t])

            qc4_c, qc4_i = qc4(mat_list, i)
            qc4_outlier.append(qc4_c)
            print("QC4 Count: ", qc4_c)
            for t in range(0, len(fnames)):
                if qc4_i[t] == 1:
                    print(fnames[t])

            #pickle.dump(qc1_outlier, open('qc1_outlier.p', 'wb'))
            #pickle.dump(qc2_outlier, open('qc2_outlier.p', 'wb'))
            #pickle.dump(qc3_outlier, open('qc3_outlier.p', 'wb'))
            pickle.dump(qc4_outlier, open('qc4_outlier.p', 'wb'))
    print("Done !!!")

    '''
    plt.subplot(2, 2, 1)
    plt.title("QC1")
    plt.xlabel("threshold")
    plt.ylabel("number of outlier")
    plt.subplots_adjust(bottom=0.5)
    plt.plot(threshold, qc1_outlier)
    plt.subplot(2, 2, 2)
    plt.title("QC2")
    plt.xlabel("threshold")
    plt.ylabel("number of outlier")
    plt.subplots_adjust(bottom=0.5)
    plt.plot(threshold, qc2_outlier)
    plt.subplot(2, 2, 3)
    plt.title("QC3")
    plt.xlabel("threshold")
    plt.ylabel("number of outlier")
    plt.plot(threshold, qc3_outlier)
    plt.subplot(2, 2, 4)
    plt.title("QC4")
    plt.xlabel("threshold")
    plt.ylabel("number of outlier")
    plt.plot(threshold, qc4_outlier)

    pylab.savefig('qc.png')
    plt.show()
    '''





