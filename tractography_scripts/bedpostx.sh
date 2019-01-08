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
probtrackParam="-P ${probtrackSampleSize} --steplength=0.75 --sampvox=0.5"
ExtractLabelSurfaceDir="/proj/NIRAL/tools"
########################################################################
var=$nr
scriptDir=$(dirname $0)
echo $scriptDir
#### Variables ##
rm $var/stdout.out
rm $var/stderr.err
echo "Parameters : $1 $2 $3 $4 $5 $6 $7 $8 $9"
#Maximum number of ROIS in parcellation table
number_ROIS=152

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

#Create subject DIR 
mkdir $var/$SUBJECT
#Copy JSON table in subject DIR 
TABLE_name=$(basename ${PARCELLATION_TABLE})
NEWPARCELLATION_TABLE=$var/$SUBJECT/${TABLE_name}
cp ${PARCELLATION_TABLE} ${NEWPARCELLATION_TABLE}

#Create Diffusion data for bedpostx 
echo "Wait 2m ..."
#sleep 1m
echo "End wait 2m" 
echo "Create Diffusion data ..."
DiffusionData=$var/$SUBJECT/Diffusion/data.nii.gz
DiffusionBrainMask=$var/$SUBJECT/Diffusion/nodif_brain_mask.nii.gz
if [ -e $DiffusionData ] && [ -e $DiffusionBrainMask ]; then 
  #Check if already process
  echo "Diffusion Data already created "
else
  mkdir $var/$SUBJECT/Diffusion
  echo "DWIConvert : nodif_brain_mask.nii.gz"
  DWIConvert --inputVolume ${BRAINMASK} --conversionMode NrrdToFSL --outputVolume ${DiffusionBrainMask} --outputBVectors $var/${SUBJECT}/Diffusion/bvecs.nodif --outputBValues $var/${SUBJECT}/Diffusion/bvals.temp

  echo "DWIConvert : data.nii.gz"
  DWIConvert --inputVolume ${DWI} --conversionMode NrrdToFSL --outputVolume ${DiffusionData} --outputBVectors $var/${SUBJECT}/Diffusion/bvecs --outputBValues $var/${SUBJECT}/Diffusion/bvals  
  echo "Create Diffusion data done !"
  if [ ! -e $DiffusionData ] || [ ! -e $DiffusionBrainMask ] || [ ! -e $var/${SUBJECT}/Diffusion/bvecs ] || [ ! -e $var/${SUBJECT}/Diffusion/bvals ]; then
    echo ERROR_PIPELINE_PROBTRACKBRAINCONNECTIVITY
  else 
    echo "Create diffusion data done !" 
  fi
fi
 

#Bedpostx 
echo "Run bedpostx ...${var}/${SUBJECT}/Diffusion ${bedpostxParam}"
command="bedpostx ${var}/${SUBJECT}/Diffusion ${bedpostxParam}"
echo $command
eval $command
echo "Bedpostx done !"

#Create labelSurfaces 
mkdir $var/${SUBJECT}/OutputSurfaces${overlapName}
SURFACES=$var/${SUBJECT}/OutputSurfaces${overlapName}/labelSurfaces

if [ -d ${SURFACES} ]; then
  echo "Label already created"
else
  cd $var/${SUBJECT}/OutputSurfaces${overlapName}
  if [ "${ignoreLabel}" = "true" ]; then 
    ignoreFlag="--ignoreLabel"
    labelID="0"
    echo "${ExtractLabelSurfaceDir}/./ExtractLabelSurfaces --extractPointData --translateToLabelNumber --labelNameInfo $var/${SUBJECT}/OutputSurfaces${overlapName}/labelListName.txt --labelNumberInfo  $var/${SUBJECT}/OutputSurfaces${overlapName}/labelListNumber.txt --useTranslationTable --labelTranslationTable ${NEWPARCELLATION_TABLE} -a ${labelSetName} --vtkLabelFile ${EXTRA_SURFACE_COLOR} --createSurfaceLabelFiles --vtkFile ${SURFACE} ${overlapFlag} ${ignoreFlag} \"${labelID}\" "
     ${ExtractLabelSurfaceDir}/./ExtractLabelSurfaces --extractPointData --translateToLabelNumber --labelNameInfo $var/${SUBJECT}/OutputSurfaces${overlapName}/labelListName.txt --labelNumberInfo  $var/${SUBJECT}/OutputSurfaces${overlapName}/labelListNumber.txt --useTranslationTable --labelTranslationTable ${NEWPARCELLATION_TABLE} -a ${labelSetName} --vtkLabelFile ${EXTRA_SURFACE_COLOR} --createSurfaceLabelFiles --vtkFile ${SURFACE} ${overlapFlag} ${ignoreFlag} "${labelID}"
  else
    echo " Testing : ${ExtractLabelSurfaceDir}"
    echo "${ExtractLabelSurfaceDir}/./ExtractLabelSurfaces --extractPointData --translateToLabelNumber --labelNameInfo $var/${SUBJECT}/OutputSurfaces${overlapName}/labelListName.txt --labelNumberInfo  $var/${SUBJECT}/OutputSurfaces${overlapName}/labelListNumber.txt --useTranslationTable --labelTranslationTable ${NEWPARCELLATION_TABLE} -a ${labelSetName} --vtkLabelFile ${EXTRA_SURFACE_COLOR} --createSurfaceLabelFiles --vtkFile ${SURFACE} ${overlapFlag}"
    ${ExtractLabelSurfaceDir}/./ExtractLabelSurfaces --extractPointData --translateToLabelNumber --labelNameInfo ${SUBJECT}/OutputSurfaces${overlapName}/labelListName.txt --labelNumberInfo  ${SUBJECT}/OutputSurfaces${overlapName}/labelListNumber.txt --useTranslationTable --labelTranslationTable ${NEWPARCELLATION_TABLE} -a ${labelSetName} --vtkLabelFile ${EXTRA_SURFACE_COLOR} --createSurfaceLabelFiles --vtkFile ${SURFACE} ${overlapFlag}
  fi
  if [ ! -d ${SURFACES} ]; then
    echo ERROR_PIPELINE_PROBTRACKBRAINCONNECTIVITY
  else
    echo "Surfaces extraction done!"	
  fi
fi

cd $var 
#Write seed list 
if [ ! -e  $var/${SUBJECT}/seeds.txt ]; then

  command="python $var/writeSeedList.py ${SUBJECT} ${overlapName} ${NEWPARCELLATION_TABLE} ${number_ROIS}"
  echo $command
  eval $command

fi

if [ ! -e  $var/${SUBJECT}/seeds.txt ]; then
 echo ERROR_PIPELINE_PROBTRACKBRAINCONNECTIVITY
else
 echo "Creation of seed list done ! "
fi

