import math
import os
from os.path import join
import numpy as np


def readMatrixFromTextFile(fname):
    print("Reading File: " + fname)
    a = []
    fin = open(fname, 'r')
    for line in fin.readlines():
        a.append([float(x) for x in line.split()])

    a = np.asarray(a)
    return a


def readMatricesFromDirectory(directory, normalize=True):
    files = [f for f in os.listdir(directory)]
    files.sort()
    mat_list = []
    for file in files:
        a = readMatrixFromTextFile(join(directory, file))
        if normalize:
            a /= a.sum(axis=1)
        else:
            a /= a.sum()
        mat_list.append(a)

    return mat_list, files

def groupElementsOfMatrices(input_mat_list):
    mat_list = []
    i = 1
    for mat in input_mat_list:
        mat_list.append(np.asarray(mat).flatten().tolist())
        i = i + 1

    element_list = []
    for j in range(0, len(mat_list[0])):
        el = []
        for i in range(0, len(mat_list)):
            el.append(mat_list[i][j])
        element_list.append(el)

    return element_list


def findMeanAndStd(mat_list):
    dim = len(mat_list[0])
    element_list = groupElementsOfMatrices(mat_list)
    stddev = [np.std(element_list[i]) for i in range(0, dim*dim)]
    meanind = [np.average(element_list[i]) for i in range(0, dim*dim)]

    return np.array(meanind).reshape(dim, dim), np.array(stddev).reshape(dim, dim)


def generateListFromMeanAndStd(listMean, listStd):
    generatedList = [np.random.normal(listMean[i], listStd[i], 1) for i in range(0, len(listMean))]
    return generatedList

def generateFakeMatrix(matrix, stdDev, ind, size):
    x, y = ind
    lx, ly = size
    new_matrix = np.zeros(matrix.shape)
    for i in range(x, x + lx):
        for j in range(y, y + ly):
            new_matrix[i][j] = np.random.normal(matrix[i][j], stdDev[i][j], 1)

    return new_matrix


def generateFakeMatrices(directory, stdDev):
    files = [f for f in os.listdir(directory)]
    mat_list = []
    for file in files:
        a = readMatrixFromTextFile(join(directory, file))
        a /= a.sum(axis=1)
        fake_mat = generateFakeMatrix(a, stdDev, (74, 0), (74, 74))
        np.savetxt(join(os.pardir, 'fake_matrix/' + file.split('.')[0] + '_fake.txt'), fake_mat)


if __name__ == '__main__':
    mat_dim = 148
    folder = input('Matrix Dir: ')
    mean, std_dev = findMeanAndStd(join(os.pardir, folder))
    generatedList = generateListFromMeanAndStd(mean, std_dev)
    mean = np.array(mean).reshape(mat_dim, mat_dim)
    std_dev = np.array(std_dev).reshape(mat_dim, mat_dim)
    print(
        'Mean Shape: ', mean.shape,
        'std_dev: ', std_dev.shape
    )
    matrix = readMatrixFromTextFile(join(os.pardir, 'matrix/S100790_fdt_network_matrix'))
    matrix /= matrix.sum(axis=1)
    generateFakeMatrices(join(os.pardir, folder), std_dev)
    '''print(
        '\nMean : ', mean,
        '\nStd dev : ', std_dev
    )'''
