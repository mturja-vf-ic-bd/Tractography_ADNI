#!/bin/bash

subDir=$1
debug=$2
current_Dir=`pwd`
echo "In directory: $current_Dir"
cmake $current_Dir/EditLabel
make -C $current_Dir/EditLabel/ -j4
cmake $current_Dir/EditParcellationTable
make -C $current_Dir/EditParcellationTable/ -j4
$current_Dir/EditLabel/./relabelVtk.sh $subDir $current_Dir/EditLabel $debug
$current_Dir/EditParcellationTable/./run.sh $subDir $current_Dir/EditParcellationTable $debug
