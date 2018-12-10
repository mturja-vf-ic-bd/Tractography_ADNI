# Tractography_ADNI

## Description
This is a pipeline to run tractography on ADNI data located on ares.ia.unc.edu:/ASD/Martin_Data/ADNI/DTI_FS_CoregData. First the labels of the surface (lh.white_labeled.vtk and rh.white_labeled.vtk) are updated according to lh_map.txt and rh_map.txt. Then both the hemisphere are combined into one file. Parcellation Table is generated for each subject which is used for visualization.

## Tools
1. FSL (bedpostx and probtractx)

## Pipeline
