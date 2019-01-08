#!/bin/bash

module add dtiprep
module add fsl/5.0.10
export OMP_NUM_THREADS=8
sub_dir=$1
output_dir=$nr

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

for file in ${subjects[@]}; do
	isbpxfinished=`./isbpxfinished.sh $file`
	isptxfinished=`./isptxfinished.sh $file`
	isRunning=`./isRunning.sh mturja $file`
	if [ $isbpxfinished = "1" ] && [ $isptxfinished = "0" ] && [ $isRunning = "0" ];
	then
		echo "${file}: job submitted"
		sed -i '/\/1.asc/d' $output_dir/$file/seeds.txt
		sed -i '/\/77.asc/d' $output_dir/$file/seeds.txt
		echo `more ${output_dir}/${file}/seeds.txt | wc -l`
		command="sbatch -p general -N 1 -n 1 -t 10-00:00:00 --mem=16g --job-name=${file}_ptx --output=${file}_ptx.txt --mail-type=END --mail-user=mturja@cs.unc.edu ./tractographyScriptApp.sh $file $sub_dir/$file/DTI/${file}_DWI.nrrd $sub_dir/$file/DTI/${file}_T1_regDTI.nrrd $sub_dir/$file/DTI/${file}_resampled_brain_mask.nrrd $sub_dir/$file/DTI/parcellationTable.json $sub_dir/$file/DTI/combined.InnerSurface_relabeled.vtk $sub_dir/$file/DTI/combined.InnerSurface_relabeled.vtk 3000 0"
		#echo $command
		eval $command
	elif [ $isptxfinished = "1" ]; then
		echo "$file already processed"
	elif [ $isbpxfinished = "0" ]; then
		echo "$file: bedpostx not finished"
	elif [ $isRunning = "1" ]; then
		echo "$file: is running already"
	elif [ ! -f ${sub_dir}/${file}/DTI/parcellationTable.json ]; then
		echo "$file: ${sub_dir}/${file}/DTI/parcellationTable.json not present"
	else
		echo "${file}: Unknown error"
	fi
done
	




