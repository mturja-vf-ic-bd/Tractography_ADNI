#!/bin/bash

for file in `ls $pn`; do
	a=`./isbpxfinished.sh $file`
	b=`./isptxfinished.sh $file`
	c=`./isRunning.sh mturja $file`
	d=`./isbpxrunning.sh $file`
	echo "${file}: ${a} ${d} ${b} ${c}"
done

