#!/bin/bash

subjectDir=$1
scriptDir=$2
debug=$3

for file in `ls $subjectDir`; do
	source=$subjectDir/$file/combined.InnerSurface_relabeled.vtk
	if [ -f $source ]
	then
		echo '$scriptDir/./EditParcellationTable '$source' '$subjectDir/$file' '$debug
		${scriptDir}/./EditParcellationTable $source $subjectDir/$file $debug
		python ${scriptDir}/rewriteTable.py $subjectDir/$file $subjectDir/parcellationTable.json
	else
		echo 'Error: vtk file missing'
	fi
done
