import os, sys, csv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import spearmanr

'''
Script to look at the relationship between AF2 scores and time from start
'''

###########################################
# Function Definitions
###########################################

def writeScoreCSV(lines):
    data_rows = []
    output_csv = 'af2750Out.csv'

    for line in lines: # Process each line in the file
        if line.startswith('SCORE:'):
            # Remove 'SCORE: ' from the start of the line
            cleaned_line = line[len('SCORE:'):].strip()
            # Split the line into columns based on spaces
            columns = cleaned_line.split()
            # Add the processed line to the data rows list
            data_rows.append(columns)

    # Separate headers from data, the rest is the actual data
    headers = data_rows[0] # First row contains headers
    headers.append("temperature") #This tells how many increments of 0.00000005
    data = data_rows[1:]

    # Write the output to a CSV file
    with open(output_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        if csvfile.tell() == 0:
            writer.writerow(headers)
        # Write the data rows
        writer.writerows(data)

    return

def plotTimevsScore():
    '''
    Function to plot the AF2 score vs the overall time elapsed. The goal is to see how (or if) scores
    trend in a certain direction with time.

    At the end, a spearman correlation is calculated to see if there is a significant relationship between
    score and time.
    '''

    data = pd.read_csv("scores750.csv") # CSV with time data from modified proteinMPNN script
    af2Data = pd.read_csv('af2750Out.csv') #AF2 output scores

    x = data['time_from_start'].values.reshape(-1, 1)  # Time is the independent variable (X)
    y = af2Data['pae_interaction'].values  # Score is the dependent variable (y)

    # Plot score vs time_from_start
    plt.plot(x, y, marker='o',linestyle="none")
    # Label the axes
    plt.xlabel('Time from Start')
    plt.ylabel('Score')

    # Add a title (optional)
    plt.title('Score vs Time from Start')

    # Show the plot
    plt.show()

    correlation, p_value = spearmanr(x,y)
    print(f"\n\n\n Spearman correlation: {correlation}, p_value: {p_value}\n")
    return

def doLinearRegression():
    '''
    Function to perform a linear regression on the AF2 scores vs the time from start. 
    '''
    
    data = pd.read_csv("scores750.csv") # CSV with time data from modified proteinMPNN script
    af2Data = pd.read_csv('af2750Out.csv') #AF2 output scores

    x = data['time_from_start'].values.reshape(-1, 1)  # Time is the independent variable (X)
    y = af2Data['pae_interaction'].values  # Score is the dependent variable (y)

    # Create a linear regression model
    model = LinearRegression()
    model.fit(x, y)

    # Predict y values based on the regression model
    y_pred = model.predict(x)

    # Get the slope and r^2 value
    r_squared = model.score(x, y)
    m = model.coef_[0]
    print(f"\n Linear Regression: Slope={m}, r^2={r_squared}\n\n\n")

    # Plot score vs time_from_start
    plt.plot(x, y, marker='o',linestyle="none")
    plt.plot(x, y_pred, color='red', label='Regression line')
    # Label the axes
    plt.xlabel('Time from Start')
    plt.ylabel('Score')

    # Add a title (optional)
    plt.title('Score vs Time from Start')

    # Show the plot
    plt.show()
    return

###########################################
# Function Calls and Main Code
###########################################

parentDirectory=""

# Only run the code in the below comment if you don't already have a CSV file with the scores
'''
filePath = os.path.join(parentDirectory, "experiment750.sc")
with open(filePath, 'r') as infile:
    lines = infile.readlines()
writeScoreCSV(lines) 
'''

plotTimevsScore()
doLinearRegression()