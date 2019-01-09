
import os
from os.path import join
import numpy as np
import util
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


def qc1(mat_list):
    element_list = get_elementlist_from_matlist(mat_list)
    outlier_percent = 10
    nCon, nSub = element_list.shape
    outlier_connections = element_list > 2
    outlier_connections = (outlier_connections.sum(axis=0) * 100 / nCon) > outlier_percent
    assert (outlier_connections.sum() == 0), "QC1 Failed"
    print("\nQC1 Passed")


def qc2(mat_list):
    element_list = get_elementlist_from_matlist(mat_list)
    avg = element_list.mean(axis=1)

    threshold_factor = 4
    expected_percent_outlier = 10
    nCon, nSub = element_list.shape

    count = 0
    for i in range(0, nSub):
        outlier_connections = (element_list[:, i] - threshold_factor * avg > 0)
        percent_outlier = outlier_connections.sum() * 100 / nCon
        if percent_outlier > expected_percent_outlier:
            count = count + 1

    assert (count == 0), "QC2 Failed"
    print("\nQC2 Passed")


if __name__ == '__main__':
    directory = 'AD-Data'
    mat_list = util.readMatricesFromDirectory(join(os.pardir, directory))
    dim = len(mat_list[0])
    qc1(mat_list)
    qc2(mat_list)
    '''
    
    
    '''


