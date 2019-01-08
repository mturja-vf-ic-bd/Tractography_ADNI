#!/bin/bash

sub=$1

if [ -d $nr/$sub/Diffusion.bedpostX/diff_slices ]; then
	echo "1"
else
	echo "0"
fi

