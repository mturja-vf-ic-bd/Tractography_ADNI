#!/bin/bash

root=/proj/NIRAL/users/mturja/TractographyScript
expected_mat_dim=148
for file in `ls`; do
	mat_file=$root/$file/Network_overlapping_loopcheck_3000_0/fdt_network_matrix
	command="rm -r ${root}/${file}/Diffusion{,.bedpostX}"
	if [ -e $mat_file ]; then
		mat_dim=`cat $mat_file | wc -l`
		if [ "$mat_dim" -eq "148" ]; then
			echo "Cleaning $file"
			echo $command
			eval $command
		else
			echo "$file has dim: $mat_dim (Expected ${expected_mat_dim}). Skipping"
		fi
	else
		if [ -d $root/$file/Diffusion.bedpostX/diff_slices ]; then
			echo "Cleaning $file"
			echo $command
			eval $command
		fi
	fi
done
