# amyloidBinderDesign

## Introduction and Background
In this project we sought to design short (20-30 residue) peptide sequences that bind amyloids with high affinity. These sequences are to be put onto protein-like-polymers (PLP)s to enhance binding affinity. To do this, we sought to compare various structure and sequence design tools. 

## Instructions

**Note:** *Our implementation of RFDiffusion and ProteinMPNN was forked from dlbinderdesign, developed nrbennet*

Currently all scripts available are for RFDiffusion > ProteinMPNN > AF2 pathway. These scripts are used to do various tasks, such as submitting jobs, creating sub-sets based on score ranges, and data analysis. Additionally, I have uploaded a version of the ProteinMPNN script that I have modified to return a CSV file with ProteinMPNN scores. 

## Current Results:

1. Protein MPNN score is not a predictor of AF2 pae_interaction score:
<img width="890" alt="Screenshot 2024-10-24 at 3 32 50 PM" src="https://github.com/user-attachments/assets/cbac05e0-c26a-4eb8-8433-647e2e7833df">

  * Spearman correlation indicates that there is no significant trend amongst this data, therefore we concluded that pae_interaction and proteinMPNN score have no relationship.
