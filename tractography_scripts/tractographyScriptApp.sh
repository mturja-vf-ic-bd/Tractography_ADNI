#!/bin/sh 

#DO TRACTOGRAPHY SCRIPT 

#Parameters
########################################################################
SUBJECT=$1  #ex : neo-0029-1-1year
DWI=$2
T1=$3
BRAINMASK=$4
PARCELLATION_TABLE=$5
SURFACE=$6
EXTRA_SURFACE_COLOR=$7
labelSetName="label"
ignoreLabel="true"
overlapping="true"
loopcheck="true"
bedpostxParam="-n 2"
probtrackSampleSize=$8
sampleNumber=$9
probtrackParam="-P ${probtrackSampleSize} --steplength=0.75 --sampvox=0.5"
ExtractLabelSurfaceDir="/proj/NIRAL/tools"
########################################################################
var=$(pwd)
scriptDir=$(dirname $0)
echo $scriptDir
#### Variables ##
echo "Parameters : $1 $2 $3 $4 $5 $6 $7 ${probtrackParam} $9"
#Maximum number of ROIS in parcellation table
number_ROIS=152
#name define by probtrackx2 tool
matrix=fdt_network_matrix
echo "Matrix Name : ${matrix}"

#Overlapping
if [ ${overlapping} = "true" ]; then 
	overlapFlag="--overlapping"
	overlapName="_overlapping"  
else
  overlapFlag=""
  overlapName=""  
fi
#Loopcheck
if [ "${loopcheck}" = "true" ]; then 
	loopcheckFlag="--loopcheck"
	loopcheckName="_loopcheck"
else 
  loopcheckFlag=""
  loopcheckName=""
fi


##### TRACTOGRAPHY PIPELINE #####
echo "Tool is running .. "

#Do tractography with probtrackx2
NETWORK_DIR=${SUBJECT}/Network${overlapName}${loopcheckName}_${probtrackSampleSize}_${sampleNumber}
replace="nii.gz"
t1=$T1 
T1_nifti=${t1//nrrd/$replace}
matrixFile=${NETWORK_DIR}/${matrix} 
echo "Checking for matrix file $matrixFile"
if [ -e $matrixFile ]; then
  echo "probtrackx already proceed"
else
  echo "Convert T1 image to nifti format "
  DWIConvert --inputVolume ${T1} --conversionMode NrrdToFSL --outputVolume ${T1_nifti} --outputBValues ${SUBJECT}/bvals.temp --outputBVectors ${SUBJECT}/bvecs.temp
  echo "T1 image conversion done ! "

  echo "Start probtrackx "
  echo "probtrackx2 --samples=${SUBJECT}/Diffusion.bedpostX/merged --mask=${SUBJECT}/Diffusion.bedpostX/nodif_brain_mask --seed=${SUBJECT}/seeds.txt --seedref=${T1_nifti} --forcedir --network --omatrix1 -V 1 --dir=${NETWORK_DIR} --stop=${SUBJECT}/seeds.txt ${probtrackParam} ${loopcheckFlag} --rseed=${sampleNumber}"

  probtrackx2 --samples=${SUBJECT}/Diffusion.bedpostX/merged --mask=${SUBJECT}/Diffusion.bedpostX/nodif_brain_mask --seed=${SUBJECT}/seeds.txt --seedref=${T1_nifti} --forcedir --network --omatrix1 -V 0 --dir=${NETWORK_DIR} --stop=${SUBJECT}/seeds.txt ${probtrackParam} ${loopcheckFlag} --rseed=${sampleNumber}

  if [ ! -e $matrixFile ]; then
   echo ERROR_PIPELINE_PROBTRACKBRAINCONNECTIVITY
  else 	
   echo "Probtrackx done !"
  fi
fi

#Normalize the matrix and save plot as PDF file 
#erase old matrix saved
rm ${matrixFile}_normalized.pdf
if [ -e $matrixFile ]; then
  echo "Normalize and plot connectivity matrix..."
  python $var/plotMatrix.py ${SUBJECT} ${matrixFile} ${overlapName} ${loopcheckName}
  echo "End, matrix save."
else
  echo "Output of probtrackx2 not here - error during the pipeline"
fi
echo "Pipeline done!"
