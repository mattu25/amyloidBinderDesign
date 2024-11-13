import os,csv
import subprocess as sp
import pandas as pd

'''
This script is used to filter the top 100 lowest scoring designs from each proteinMPNN score range.

The ranges being: 
    mpnnScore < 1.8
    1.8 <= mpnnScore < 1.9
    1.9 <= mpnnScore < 2.0
'''

###########################################
# Function Definitions
###########################################

def moveFiles(pdbs):
    #Move files to necessary place for AF2
    experimentDir = os.path.join(mainDir, "experiment")
    outputDir = os.path.join(mainDir, "outputs")
    os.mkdir(experimentDir)

    os.chdir(outputDir)
    for low, med, high in pdbs:
        sp.run(f"cp {low} {med} {high} {experimentDir}", shell=True)

    os.chdir(mainDir)
    return

def writeLog():
    finalData = list(zip(low10_sub1_8_pdbs,low10_sub1_8Data["score"],
                     low10_sub1_9_pdbs,low10_sub1_9Data["score"],
                     low10_sub2_0_pdbs,low10_sub2_0Data["score"]))

    csv_data = []
    for i in range(len(finalData)):
        csv_data.append((finalData[i][0], finalData[i][1]))  # From the first tuple
        csv_data.append((finalData[i][2], finalData[i][3]))  # From the second tuple
        csv_data.append((finalData[i][4], finalData[i][5]))  # From the third tuple

    # Write to CSV
    with open('experiment2Info.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['file_name', 'score'])  # Write the header
        writer.writerows(csv_data)  # Write the data

    return

###########################################
# Function Calls and Main Code
###########################################

#Define basic variables and load data 
mainDir = "/home/maunger/dl_binder_design-main/scripts/optimization2024_10_23"
data = pd.read_csv("scores.csv")

#Create subsets of the data for different score ranges
sub1_8Data = data[data["score"]<1.8]
sub1_9Data = data[(1.8 <= data["score"]) & (data["score"]<1.9)]
sub2_0Data = data[(1.9<=data["score"]) & (data["score"]<2.0)]

#Select the lowest 10 scores from each dataset
low10_sub1_8Data = sub1_8Data.nsmallest(100,"score")
low10_sub1_9Data = sub1_9Data.nsmallest(100,"score")
low10_sub2_0Data = sub2_0Data.nsmallest(100,"score")

#Select PDB files
baseFile = "20to30_batch0_23_dldesign_"

low10_sub1_8_pdbs = [baseFile+str(idx)+".pdb" for idx in low10_sub1_8Data["sequence_number"]]
low10_sub1_9_pdbs = [baseFile+str(idx)+".pdb" for idx in low10_sub1_9Data["sequence_number"]]
low10_sub2_0_pdbs = [baseFile+str(idx)+".pdb" for idx in low10_sub2_0Data["sequence_number"]]

pdbs = zip(low10_sub1_8_pdbs, low10_sub1_9_pdbs, low10_sub2_0_pdbs)

moveFiles(pdbs)
writeLog()

