#!/bin/bash

size=148
for file in `ls $pn`; do 
	if [ -f $nr/$file/seeds.txt ]; then
		#a=`more $nr/$file/seeds.txt | wc -l`; 
		ptx=`isptxfinished.sh $pn $nr/$file`;
		#bpx=`isbpxfinished.sh $pn $file`;
		#isrunning=`isRunning.sh mturja $file` 
		if [ $ptx = "1" ]; then 
			echo "$file"
		fi
	fi 
done
