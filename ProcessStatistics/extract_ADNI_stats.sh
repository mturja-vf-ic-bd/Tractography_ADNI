#!/bin/bash
# Reads statistics for each network data. For network data we have scan id's like S144552.
# But the FreeSurfer statistics has subjectID with date like ADNI_131_S_0123_20151214162609918

input=$1  # File which contains the mapping(pairedDTIList.txt)
adni_dir="mturja@ares.ia.unc.edu:/BAND/ADNI/FS_Data"
copy_dir="/home/turja/AD_stats"
while IFS= read -r var;
do
	while IFS=',' read -ra ADDR; do
		# Read subjectID and scanID.
		# Example: subjectID: ADNI_131_S_0123_20151214162609918, scanID: S144552
		subjectID="${ADDR[0]}"
		subjectID=`echo $subjectID | xargs`
		while IFS='/' read -ra SCNADDR; do
     		scanID="${SCNADDR[7]}"
     	done <<< "${ADDR[1]}"
     	echo "${subjectID} maps to ${scanID}"

     	# Now copy stat file
     	from="${adni_dir}/${subjectID}/stats/"
     	to="${copy_dir}/${scanID}/"
     	mkdir $to
     	echo "From: ${from}, To: ${to}"

     	rsync -rv $from $to

	done <<< "$var"
done < "$input"