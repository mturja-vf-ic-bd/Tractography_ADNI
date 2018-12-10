#!/bin/bash

debug=$1
root="/home/turja/Desktop/ADNI_processing"
subDir="/home/turja/Desktop/sub"
cmake $root/EditLabel
make -C $root/EditLabel/ -j4
cmake $root/EditParcellationTable
make -C $root/EditParcellationTable/ -j4
${root}/EditLabel/./relabelVtk.sh $subDir $root/EditLabel $debug
${root}/EditParcellationTable/./run.sh $subDir $root/EditParcellationTable $debug