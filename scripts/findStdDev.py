from sys import argv
import os
from os.path import isfile, join
from matplotlib import pyplot as plt
import numpy as np


os.chdir(argv[1])
std = []
mean = []
folders = [f for f in os.listdir(os.getcwd()) if not isfile(f)]
ind = [int(f.split('_')[3]) for f in folders]
folders = [f for _,f in sorted(zip(ind, folders))]
for folder in folders:
	files = [f for f in os.listdir(folder)]
	mat_list = []
	for file in files:
		a = []
		fin = open(join(folder, file), 'r')
		for line in fin.readlines():
			a.append([ float(x) for x in line.split()])

		a = np.asmatrix(a)
		a /= a.sum()
		dim = len(a.flatten().tolist()[0])
		mat_list.append(a.flatten().tolist())

	element_list = []
	for j in range(0, len(mat_list[0][0])):
		el = []
		for i in range(0, len(mat_list)):
			el.append(mat_list[i][0][j])
		element_list.append(el)
	std_dev = [np.std(element_list[i]) for i in range(0, dim)]
	mean_ind = [np.average(element_list[i]) for i in range(0, dim)]
	std.append(np.average(std_dev))
	mean.append(np.average(mean_ind))

#normalized_std = [x/y for x, y in zip(std, mean)]
normalized_std = std
print normalized_std
plt.xlabel('#seeds')
plt.ylabel('standard deviation')
plt.plot(sorted(ind), normalized_std)
plt.show()
