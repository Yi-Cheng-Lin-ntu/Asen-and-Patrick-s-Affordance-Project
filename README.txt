# fMRI RSA Project

This project analyzes the relationship between fMRI responses and behavioral ratings (grasp / hold) using Representational Similarity Analysis (RSA).

## Data

- fMRI data: subject_fMRI_nii/ (not included in repo)
- Stimuli: THINGS dataset (not included in repo)
- All of the data can be accessed in https://things-initiative.org/

## Subjects

- sub-01
- sub-02
- sub-03

## Analysis

- ROI extraction
- RDM computation
- RSA between brain and behavior

## Notes

Large datasets are excluded via .gitignore.

## Required Prerequisites
Ensure you have the following standard Python data science and neuroimaging libraries installed in your environment before running the notebook:
numpy, pandas, matplotlib, nibabel

## Modular Analysis Pipeline
Our primary analysis notebook (.ipynb) is split into a 3-Cell modular design to separate heavy data I/O from statistical plotting, ensuring efficiency and easy replication.

- Cell 1: Environment & Atlas InitializationLoads standard neuroimaging packages.Sets up dynamic global paths for subjects (sub-01, sub-02, sub-03) and targets (35 selected tool concepts).Loads the pre-resampled Brainnetome Atlas to define Regions of Interest (ROIs): AIP, IPL, vPM (Dorsal) and VVC (Ventral control).

- Cell 2: Automated RDM Extraction & Group AveragingLoops dynamically through each subject's directory, mapping condition CSVs to the nested fMRI BIDS structure.Extracts voxel activation patterns (Beta values) from all 12 sessions*10 runs (120 NIfTI files per subject).Averages the 12 trial repetitions per item to compress the data into clean 35 x 35 concept-level RDMs, minimizing trial-level visual noise.Performs a Group-Level average across all 3 subjects to eliminate individual physiological noise.

- Cell 3: Cross-Region RSA valuates Representational Connectivity within the dorsal pathway and across pathways. Automatically computes correlations (Spearman & Pearson) and generates publication-ready scatter plots for:Cross-Stream Dissociation: Ventral (VVC) vs. Dorsal ROIs. Within-Stream Connectivity: Dorsal ROIs (AIP / IPL / vPM).

