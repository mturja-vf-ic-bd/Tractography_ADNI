#!/bin/bash

user=$1
sub=$2

a=`squeue -u $user | grep $sub`
if [ "${a}0" != "0" ]; then
	isrunning=1
else
	isrunning=0
fi

echo $isrunning
