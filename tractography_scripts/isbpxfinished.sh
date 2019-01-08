#!/bin/bash

ptr=$1
finished=0
files=`ls $pn | grep $ptr`
for file in $files; do
	if [ -d $nr/$file ] && [ -d $nr/$file/Diffusion.bedpostX ]; then
		count=`ls $nr/$file/Diffusion.bedpostX/ | wc -l`
		if [ $count = "29" ]; then
			finished=1
			#echo $file
		else
			finished=0
			break
		fi
	else
			finished=0
			break
	fi
done

echo $finished

	
