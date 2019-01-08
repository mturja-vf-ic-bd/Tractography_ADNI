# Tractography_ADNI

## Description
This is a pipeline to run tractography on ADNI data located on ares.ia.unc.edu:/ASD/Martin_Data/ADNI/DTI_FS_CoregData. This directory contains destriux parcellation of brain surfaces from FreeSurfer. These surfaces have 150 regions with 150 labels (75 per hemisphere). The FreeSurfer labels are quite big and arbitrary. So, first the labels of the surfaces (lh.white_labeled.vtk and rh.white_labeled.vtk) are updated according to [map_lh.txt](EditLabel/map_lh.txt) and [map_rh.txt](EditLabel/map_rh.txt) for each hemisphere. Then both the hemisphere are combined into one file (combined.InnerSurface_relabeled.vtk). Labels for ```Unknown``` region (1, 77) are ignored later during tractography. 

Parcellation Table is generated for each subject with proper coordinate for each region of the surface for visualization purpose (Correct coordinates are needed to visualize in BrainNetViewer). Coordinate of a region is calculated by taking the average of all the points that belong to this region.

To run the tractography, ```bedpostx``` and ```probtrackx2``` (from FSL) is run on each subject consecutively.

## Input
To run this pipeline, each subject must have a directory named ```DTI``` and the following files in the ```DTI``` directory:

* DWI (ex. S100790_DWI.nrrd)
* T1 (ex. S100790_T1_regDTI.nrrd)
* Brain mask (ex. S100790_resampled_brain_mask.nrrd)
* lh.white_labeled.vtk
* rh.white_labeled.vtk
* Parcellation Table (parcellationTable.json)

## Output
The output of the pipeline is a 148 x 148 connectivity matrix. However, It also generates lots of intermediate files. For each subject the pipeline will create a folder and the folder will contain the following files:

* Diffusion
* Diffusion.bedpostX
* Network_overlapping_loopcheck_3000_0
* OutputSurfaces_overlapping
* parcellationTable.json
* seeds.txt

The connectivity matrix is named ```fdt_network_matrix``` and it resides in ```Network_overlapping_loopcheck_3000_0```

## Dependencies
* cmake > 3.0.0
  - I am using 3.13.1
* VTK 
  - To install VTK, follow this link: https://www.vtk.org/Wiki/VTK/Building/Linux
  - add the ```bin``` and ```lib``` folder in the ```PATH``` and ```LD_LIBRARY_PATH``` environmental variable
  - Tested with VTK-6.1.0, VTK-8.2.0
* FSL (bedpostx and probtractx)
* dtiprep

## Pipeline Overview
Add image here

## Installation
```export pn=<subject_dir>
   export nr=<output_dir>
```
```git clone https://github.com/mturja-vf-ic-bd/Tractography_ADNI.git
   cd Tractography_ADNI
   ./run_pipeline.sh <subject_dir> <debug>
```
Copy all the scripts to <output_dir>
To run bedpostx: ```./submit_job.sh (<subject_name1>) (<subject_name2>) ...```
If no subject_name is given, bedpostx is run for all the subjects.

To run tractography: ```./submit_job_trac.sh (<subject_name1>) (<subject_name2>) ... ```
If no subject_name is given, bedpostx is run for all the subjects.
