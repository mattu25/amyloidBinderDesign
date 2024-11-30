# amyloidBinderDesign

## Introduction and Background
In this project we sought to design short (20-30 residue) peptide sequences that bind amyloids with high affinity. These sequences are to be put onto protein-like-polymers (PLP)s to enhance binding affinity. To do this, we sought to compare various structure and sequence design tools. 

*This project is a work in progress and we are in the process of running experiments to test ESM3 and ESM-IF*

## Instructions

**Note:** *Our implementation of RFDiffusion and ProteinMPNN was forked from `dlbinderdesign`, developed by nrbennet*

Currently all scripts available are for RFDiffusion > ProteinMPNN > AF2 pathway. These scripts are used to do various tasks, such as submitting jobs, creating sub-sets based on score ranges, and data analysis. Additionally, I have uploaded a version of the ProteinMPNN script that I have modified to return a CSV file with ProteinMPNN scores. 

Here is a brief overview of each script:

* `dl_interface_design_modified`: Modified script from `dlbinderdesign` with new flag to supply output directory for proteinMPNN scores.
* `filterScores.py`: File management and organization script, used to gather structures from predefined mpnn score categories.
* `mpnnScore_AF2Score.py`: Used to generate figure 1 below.
* `scoreVsTime.py`: Track pae_interaction as a function of time (which is a proxy for the design number) -- we were finding the optimal amount of sequences to generate to get a pae_interaction score < 11.
* `temperatureVisualization.py`: Used to track different temperature values of proteinMPNN and how that affected the number of low pae_interaction compounds. This script has several methods for analyzing the data, including bootstrapping.
* `util_protein_mpnn_modified.py`: Modified script for proteinmpnn from `dlbinderdesign`
* `variedTempMPNN.py` & `variedTempAF2.py`: Scripts for running temperature experiments on the cluster. 

## Current Results:

**We are currently working on finaizing our results for temperature, however it seems raising tempearature for proteinMPNN does not have any positive impact on results**

1. Protein MPNN score is not a predictor of AF2 pae_interaction score:
<img width="890" alt="Screenshot 2024-10-24 at 3 32 50 PM" src="https://github.com/user-attachments/assets/cbac05e0-c26a-4eb8-8433-647e2e7833df">

  * Spearman correlation indicates that there is no significant trend amongst this data, therefore we concluded that pae_interaction and proteinMPNN score have no relationship.
