from sys import argv
import json
import numpy as np
from collections import OrderedDict



fileName = "destriux.json" # destriux dataframe from R
pt_name = "parcellationTable.json" # parcellation table to edit VisuOrder
#matrix_file = argv[1]

# Read detrieux to get lobe info
with open(fileName) as f:
    destriux = json.load(f)
f.close()
# Read parcellation table to edit VisuOrder
with open( pt_name) as f:
	pt = json.load(f)
f.close()
'''
#Read Matrix
fin = open(matrix_file)
matrix = []
for line in fin.readlines():
	matrix.append( [ float(x) for x in line.split()] )

matrix = np.asarray(matrix)
'''
# There should be 148 regions.
if len(pt) == 152:
	del pt[118], pt[76], pt[42], pt[0] # Delete Medial Wall and Unknown
	
order_map = dict(zip(set(destriux["lobe"]), [1, 5, 4, 6, 2, 3])) # Create a priority map for each lobe.
lobeSortedTuple = sorted(zip(destriux["name"][0:len(pt)/2], destriux["lobe"][0:len(pt)/2], destriux["index"][0:len(pt)/2]), key = lambda x:order_map[x[1]]) # Sort according to lobe priority.
#lobeSortedTuple = zip(destriux["name"][0:len(pt)/2], destriux["lobe"][0:len(pt)/2], destriux["index"][0:len(pt)/2]) # Sort according to lobe priority.
for i in range(0, len(lobeSortedTuple)):
	pt[lobeSortedTuple[i][2] - 1]["VisuOrder"] = i
	pt[lobeSortedTuple[i][2] - 1]["VisuHierarchy"] = "seed.left." + lobeSortedTuple[i][1]
	pt[lobeSortedTuple[i][2] - 1 + len(pt)/2]["VisuOrder"] = len(pt) - i - 1
	pt[lobeSortedTuple[i][2] - 1 + len(pt)/2]["VisuHierarchy"] = "seed.right." + lobeSortedTuple[i][1]


# Fix Matrix Row
for i in range(0, len(pt)):
	pt[i]["MatrixRow"] = i
	del pt[i]["labelValue"]
	if i < len(pt)/2:
		pt[i]["name"] = "l" + pt[i]["name"]
	else:
		pt[i]["name"] = "r" + pt[i]["name"]

with open('parcellationTable_Ordered.json', 'w') as outfile:
    json.dump(pt, outfile)
outfile.close()

'''
# This part is to prepare nodes and matrix for circle plot
# rearrange matrix and nodeNames according to VisuOrder
order = np.argsort([pt[i]["VisuOrder"] for i in range(0, len(pt))])
nodeNames = [pt[order[i]]["name"] for i in range(0, len(pt))]
plotDir = '/home/turja/Desktop/ADNI_processing/CirclePlot'
with open(plotDir + '/nodeNames.csv', 'w') as f:
	for n in nodeNames:
		f.write(n+",\n")

matrix = matrix[order]
matrix = matrix[:,order]


np.savetxt(plotDir + '/matrix.txt', matrix, fmt="%.3f")
'''
