#!/bin/bash

dir=$1

for file in `ls $dir`; do
	if [ ! -d $dir/$file/DTI ]; then
		echo "${file}: DTI directory not present"
	elif [ ! -f $dir/$file/DTI/${file}_DWI.nrrd ]; then
		echo "${file}: DWI not present"
	elif [ ! -f $dir/$file/DTI/${file}_T1_regDTI.nrrd ]; then
		echo "${file}: T1 not present"
	elif [ ! -f $dir/$file/DTI/${file}_resampled_brain_mask.nrrd ]; then
		echo "${file}: brain mask not present"
	elif [ ! -f $dir/$file/DTI/parcellationTable.json ]; then
		echo "${file}: parcellationTable not present"
	elif [ ! -f $dir/$file/DTI/combined.InnerSurface_relabeled.vtk ]; then
		echo "$file: combined.InnerSurface_relabeled.vtk not present"
	else
		echo "$file: test passed"
	fi
done
