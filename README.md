# Tractography_ADNI

## Description
This is a pipeline to run tractography on ADNI data located on ares.ia.unc.edu:/ASD/Martin_Data/ADNI/DTI_FS_CoregData. This directory contains destriux parcellation of brain surfaces from FreeSurfer. These surfaces have 152 regions with 152 labels (76 per hemisphere). The FreeSurfer labels are quite big and arbitrary. So, first the labels of the surfaces (lh.white_labeled.vtk and rh.white_labeled.vtk) are updated according to [map_lh.txt](EditLabel/map_lh.txt) and [map_rh.txt](EditLabel/map_rh.txt) for each hemisphere. Then both the hemisphere are combined into one file (combined.InnerSurface_relabeled.vtk). Labels for ```Unknown``` and ```Medial Wall``` (0, 1, 76, 77) are ignored later during tractography. 

Parcellation Table is generated for each subject with proper coordinate for each region of the surface for visualization purpose (Correct coordinates are needed to visualize in BrainNetViewer). Coordinate of a region is calculated by taking the average of all the points that belong to this region.

To run the tractography, ```bedpostx``` and ```probtrackx2``` (from FSL) is run on each subject consecutively.

## Input

## Tools
1. FSL (bedpostx and probtractx)

## Pipeline Overview
Add image here

## Installation

```git clone https://github.com/mturja-vf-ic-bd/Tractography_ADNI.git
   cd Tractography_ADNI
   ./run_pipeline.sh <subject_dir> <debug>
```
