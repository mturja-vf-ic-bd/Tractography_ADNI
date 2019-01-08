#!/bin/bash

module add dtiprep
module add fsl/5.0.10

sub_dir=$1

if [ $# -gt 1 ]
then
	i=0
	c=0
	for args in $@; do
		if [ $c -gt 0 ]
		then
			for s in `ls -a ${sub_dir} | cat | grep ${args}`; do
				subjects[`expr $i`]=$s
				i=`expr $i + 1`
			done
		fi
		c=`expr $c + 1`
	done
else
	subjects=`ls $sub_dir`
fi

echo "Subjects: ${subjects[@]}"
for file in ${subjects[@]}; do
	isfinishedbpx=`./isbpxfinished.sh $file`
	isfinishedptx=`./isptxfinished.sh $file`
	echo "$file --> BPX: $isfinishedbpx, PTX: $isfinishedptx"
	if [ $isfinishedbpx = "0" ] && [ $isfinishedptx = "0" ]
	then
		#rm -r ${file}
		echo "Submitting bedpostx for ${file}"
		command="sbatch -p general -N 1 -n 1 -t 3-00:00:00 --mem=4g --job-name=${file}_bpx --output=${file}_bpx.txt --mail-type=END --mail-user=mturja@cs.unc.edu ./bedpostx.sh $file $sub_dir/$file/DTI/${file}_DWI.nrrd $sub_dir/$file/DTI/${file}_T1_regDTI.nrrd $sub_dir/$file/DTI/${file}_resampled_brain_mask.nrrd $sub_dir/$file/DTI/parcellationTable.json $sub_dir/$file/DTI/combined.InnerSurface_relabeled.vtk $sub_dir/$file/DTI/combined.InnerSurface_relabeled.vtk"	
		echo $command
		eval $command
	else
		echo "Skipping: $file"
	fi
done
