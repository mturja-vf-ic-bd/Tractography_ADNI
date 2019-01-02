#!/bin/bash

subject_Dir=$1
scriptDir=$2
debug=$3

for file in `ls $subject_Dir`; do
	source=$subject_Dir/$file/DTI/combined.InnerSurface_relabeled.vtk
	if [ -f $source ]
	then
		${scriptDir}/./EditParcellationTable $source $subject_Dir/$file/DTI $debug
		python ${scriptDir}/rewriteTable.py $subject_Dir/$file/DTI $subject_Dir/parcellationTable.json
	else
		echo 'Error: vtk file missing'
	fi
done
