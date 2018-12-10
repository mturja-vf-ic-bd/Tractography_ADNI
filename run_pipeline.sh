#!/bin/bash

subDir=$1
debug=$2
cmake EditLabel
make -C EditLabel/ -j4
cmake EditParcellationTable
make -C EditParcellationTable/ -j4
EditLabel/./relabelVtk.sh $subDir EditLabel $debug
EditParcellationTable/./run.sh $subDir EditParcellationTable $debug