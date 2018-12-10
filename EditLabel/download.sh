#!/bin/bash
# Script to download all the necessary file from the server

source=$1
target=$2
lh_white="lh.white_labeled.vtk"
rh_white="rh.white_labeled.vtk"
relabel="./EditVtk"

for file in `ls $target`; do
	lh_file=$source$file/DTI/$lh_white
	rh_file=$source$file/DTI/$rh_white
	combined_file=$source$file/DTI/combined.InnerSurface_relabeled.vtk
	echo trans for $file
	echo $lh_file
	echo $rh_file
	rsync -v $lh_file $target$file
	rsync -v $rh_file $target$file
done