#!/bin/bash

for file in `ls $pn`; do 
	a=`./isptxfinished.sh $pn $file`
	if [ $a = "1" ]; then
		rsync -rv $nr/$file/Network_overlapping_loopcheck_3000_0/fdt_network_matrix $nr/../ADNI_matrix/${file}_fdt_network_matrix
	fi
done
