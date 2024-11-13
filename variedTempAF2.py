import os
import subprocess as sp

parentDir='/home/maunger/dl_binder_design-main/scripts/temperatureTests2024_11_9'

mainSubDir = os.path.join(parentDir,"temperatureExperiment")

for file in os.listdir(mainSubDir):
	pdbdir = os.path.join(mainSubDir, str(file))
	outputDir = os.path.join(mainSubDir, str(file)+"_AF2")
	scoreFile = os.path.join(parentDir, str(file)+"_AF2Scores.sc")

	with open("af2Script.sh", "w") as script:
		instructions = f'''#!/bin/bash
#SBATCH --nodes=1                     
#SBATCH --partition=gpu               
#SBATCH --ntasks-per-node=1           
#SBATCH --gres=gpu:1    
#SBATCH --time=5:00:00
#SBATCH --job-name=AF2
#SBATCH --mail-user="matthew_unger@lifesci.ucsb.edu"
#SBATCH --mail-type=FAIL

mkdir experiment2_af2Scores

python3 ~/dl_binder_design-main/af2_initial_guess/predict.py -pdbdir {pdbdir} -outpdbdir {outputDir} -scorefilename {scoreFile}
	'''
			
		script.writelines(instructions)

	sp.call("chmod +x af2Script.sh", shell=True)
	sp.call("sbatch af2Script.sh", shell=True)
