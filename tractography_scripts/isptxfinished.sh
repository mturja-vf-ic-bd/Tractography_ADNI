#!/bin/bash

ptr=$1

finished=0
for file in `ls $pn | grep $ptr`; do
	finished=0
	if [ -e $nr/$file/Network_overlapping_loopcheck_3000_0/fdt_network_matrix ]; then
		finished=1
	fi
	echo $finished
	#echo "${file}: ${finished}"
done

