#!/bin/bash
# Script to relabel all the vtk files in a specific directory

search_Dir=$1
script_Dir=$2
debug=$3
lh_white="lh.white_labeled.vtk"
rh_white="rh.white_labeled.vtk"
relabel="${script_Dir}/./EditVtk"

for file in `ls $search_Dir`; do
	lh_file="$search_Dir/$file/$lh_white"
	rh_file="$search_Dir/$file/$rh_white"
	combined_file="$search_Dir/$file/combined.InnerSurface_relabeled.vtk"
	echo $lh_file, $rh_file, $combined_file
	if [ -f $lh_file ] && [ -f $rh_file ]
	then
		$relabel $lh_file $rh_file $combined_file $debug
	else
		echo 'Required file not found for '$file
	fi

	if [ -f $combined_file ]
	then
		echo "Successful "$file
	else
		echo "Something went wrong with "$file
	fi
done
