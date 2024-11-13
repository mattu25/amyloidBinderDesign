import os
import subprocess as sp
import numpy as np

parentDir='/home/maunger/dl_binder_design-main/scripts/temperatureTests2024_11_9'

pdbDir = os.path.join(parentDir, "testPDB")
mainOutputDir = os.path.join(parentDir, "temperatureExperiment") 
scoreCSV = os.path.join(parentDir, "scores.csv")
os.mkdir(mainOutputDir)

# Create a range of 20 temperature values with np.arange starting at 0.000001 and ending at 1

# Create a range of 10 temperatures starting from 0.000001 and increasing by orders of magnitude until 100
# 10/31: tempValues = np.linspace(0.000001, 100, num=10)
# 11/1: tempValues = np.linspace(0.000001, 0.000002, num=10)
# 11/3A: tempValues = np.linspace(0.000001, 10, num=20)
# 11/3B: tempValues = np.linspace(-np.log10(start_value), -np.log10(end_value), 20)

log_values = np.linspace(-np.log(0.000001), -np.log(100), 20)
tempValues = [np.exp(-val) for val in log_values]

for temp in tempValues:
	outputDir = os.path.join(mainOutputDir, f"pTemp_{-1 * np.log(temp)}")
	localPDB = os.path.join(outputDir,"pdbsOriginal")
	submitDir = os.path.join(outputDir,"submit")
	os.mkdir(outputDir)
	os.mkdir(localPDB)
	os.mkdir(submitDir)
	sp.run(f"cp {pdbDir}/*.pdb {localPDB}", shell=True)
	os.chdir(submitDir)

	with open("mpnnScript.sh", "w") as script:
		instructions = f'''#!/bin/bash
#SBATCH --nodes=1                     
#SBATCH --partition=gpu               
#SBATCH --ntasks-per-node=1           
#SBATCH --gres=gpu:1  
#SBATCH --time=02:00:00
#SBATCH --job-name=MPNN
#SBATCH --mail-user="matthew_unger@lifesci.ucsb.edu"
#SBATCH --mail-type=FAIL

python3 ~/dl_binder_design-main/mpnn_fr/dl_interface_design.py -outputScores {scoreCSV} -pdbdir {localPDB} -relax_cycles 0 -seqs_per_struct 100 -checkpoint_path /home/maunger/dl_binder_design-main/mpnn_fr/ProteinMPNN/soluble_model_weights/v_48_020.pt -temperature {float(temp)} -outpdbdir {outputDir} 
'''
		script.writelines(instructions)
	
	sp.call("chmod +x mpnnScript.sh", shell=True)
	sp.call("sbatch mpnnScript.sh", shell=True)

	os.chdir(mainOutputDir)