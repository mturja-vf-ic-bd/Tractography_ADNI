import json
from pprint import pprint
import sys
import csv

sub_dir = sys.argv[1]
coord_map = sub_dir+'/coord_map'
table = sys.argv[2]

# Read json
with open(table) as f:
	data = json.load(f)

# Read CSV map
c_map = {}
with open(coord_map) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        c_map[row[0].strip()] = [float(row[1].strip()), float(row[2].strip()), float(row[3].strip())]


for i in range(0, len(data)):
	key = data[i]['labelNumber']
	if key in c_map.keys():
		data[i]['coord'] = c_map[key]
	else:
		print 'Not found ', data[i]['name']

with open(sub_dir+'/parcellationTable.json', 'wb') as outFile:
	json.dump(data, outFile)

