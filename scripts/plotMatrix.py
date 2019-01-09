import numpy as np
import matplotlib
import math
matplotlib.use('Agg')
from matplotlib import pylab as pl
from sys import argv
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt

#args : ${SUBJECT} ${network_DIR} ${overlapName} ${loopcheck}
fileMatrix = argv[1]
lowerLimit =  argv[2]
upperLimit = argv[3]
normalize_flag = 1

#fileMatrix = subject + '/Network' + overlapName + loopcheck + '/' + matrix
fin = open(fileMatrix,'r')
a=[]
for line in fin.readlines():
  a.append( [ float(x) for x in line.split() if x != "\n" ] )   

a = np.asmatrix(a, float)
if normalize_flag == 1:
	# Normalize and triangulate
	a = (a + a.transpose())/2
	a /= a.sum(axis=1)
	np.savetxt(fileMatrix + '_row_normalized', a, fmt='%f')

#a = -np.log10(a)
# plotting the correlation matrix
fig = pl.figure(num=None, figsize=(8, 8))
fig.clf()
plt.xlabel('Seeds')
plt.ylabel('Targets')
ax = fig.add_subplot(1,1,1)
cax = ax.imshow(a, interpolation='nearest', vmin=lowerLimit, vmax=upperLimit)
fig.colorbar(cax)
fig.savefig(fileMatrix + '_row_normalized.pdf', format='pdf')
