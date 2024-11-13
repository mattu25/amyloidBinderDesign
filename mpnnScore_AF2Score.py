import os, sys, csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import spearmanr

'''
Script to compare MPNN scores with AF2 scores
'''

###########################################
# Function Definitions
###########################################

def writeScoreCSV(lines):
    data_rows = []
    output_csv = 'experiment2Scores.csv'

    for line in lines: # Process each line in the file
        if line.startswith('SCORE:'):
            # Remove 'SCORE: ' from the start of the line
            cleaned_line = line[len('SCORE:'):].strip()
            # Split the line into columns based on spaces
            columns = cleaned_line.split()
            # Add the processed line to the data rows list
            data_rows.append(columns)

    # Separate headers from data, the rest is the actual data
    headers = data_rows[0]  # First row contains headers
    data = data_rows[1:]  

    # Write the output to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        writer.writerow(headers)
        # Write the data rows
        writer.writerows(data)

    return

def generateMergedData(mpnnData, af2Data):
    af2Data['description'] = af2Data['description'].str.replace('_af2pred', '.pdb', regex=False)
    mpnnData.rename(columns={"score": "mpnnScore"}, inplace=True)
    mergedData = pd.merge(mpnnData, af2Data, left_on="file_name", right_on='description', how="inner")
    return mergedData

def generateViolinPlot(mergedData):
    sub1_8MPNNscores = mergedData[mergedData["mpnnScore"]<1.8]
    sub1_9MPNNscores = mergedData[(1.8 <= mergedData["mpnnScore"]) & (mergedData["mpnnScore"]<1.9)]
    sub2_0MPNNscores = mergedData[(1.9 <= mergedData["mpnnScore"]) & (mergedData["mpnnScore"]<2.0)]
    
    af2Scores = [sub1_8MPNNscores["pae_interaction"],
                sub1_9MPNNscores["pae_interaction"], 
                sub2_0MPNNscores["pae_interaction"]]
    
    fig, ax = plt.subplots()
    parts = ax.violinplot(af2Scores, showmeans=False, showmedians=True)

    # Show data points as scatter plot on top of the violin plot
    for i, dataset in enumerate(af2Scores, start=1):
    # Adding random noise along the x-axis for better visibility
        ax.scatter(np.full_like(dataset, i), dataset, alpha=0.6, color='black', s=10)
    
    ax.set_xticks([1, 2, 3], ['MPNN Score < 1.8', '1.8 <= MPNN Score < 1.9', ' 1.9 <= MPNN Score < 2.0'])
   
    plt.title("AF2 Scores By Top 100 MPNN Scores")
    plt.ylabel("pae_interaction")
    plt.xlabel("MPNN Score Range")
    
    plt.show()

    return

def generateScorePlot(mergedData):
    plt.scatter(mergedData["mpnnScore"], mergedData["pae_interaction"], c="blue")
    plt.xlabel('MPNN Score')
    plt.ylabel('pae_interaction')
    plt.title('MPNN Score vs pae_interaction Scatter Plot')
    plt.show()

    correlation, p_value = spearmanr(mergedData["mpnnScore"], mergedData["pae_interaction"])
    print(f"\n\n\nSpearman correlation: {correlation}, p_value: {p_value}\n\n\n")
    return

###########################################
# Function Calls and Main Code
###########################################

# Define parent directory
parentDirectory=""

#if "experiment1Info.csv" not in os.listdir(parentDirectory):

with open('experiment2.sc', 'r') as infile: #Remember to change this to correct .sc file
    lines = infile.readlines()
writeScoreCSV(lines)

experiment1Info = pd.read_csv("experiment2Info.csv") #Will need to match output csv name given in writeScoreCSV 
experiment1IScores = pd.read_csv("experiment2Scores.csv")

data = generateMergedData(experiment1Info, experiment1IScores)
generateViolinPlot(data)
generateScorePlot(data)