import os, sys, csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit

###########################################
# Function Definitions
###########################################

def writeScoreCSV(lines, outCSV, filename=None):
    data_rows = []
    output_csv = outCSV

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

    if filename != None:
        #t = np.exp(-1*float(filename[6:].strip("_AF2Scores.sc")))
        t = np.round(float(filename.replace("pTemp_", "").replace("_AF2Scores.sc", "")), 3)
        data = [row + [t] for row in data]

    # Write the output to a CSV file
    with open(output_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        if csvfile.tell() == 0:
            writer.writerow(headers)
        # Write the data rows
        writer.writerows(data)

    return

def makeViolinPlot(dataFile):

    data = pd.read_csv(dataFile)

    temperatures = data["temperature"].unique()
    temperatures = np.sort(temperatures)[::-1]
    data_by_temp = [data[data["temperature"] == temp]['pae_interaction'].values for temp in temperatures]
    
    plt.figure(figsize=(8, 6))
    plt.violinplot(data_by_temp)
    
    plt.xticks(range(1, len(temperatures) + 1), temperatures)
    # Add labels and title
    plt.xlabel("-log(Temperature)")
    plt.ylabel("PAE Interaction")
    plt.title("PAE Interaction by Temperature")

    plt.show()
    return

def makeBoxPlot(dataFile):
    data = pd.read_csv(dataFile)
    temperatures = data["temperature"].unique()
    temperatures = np.sort(temperatures)[::-1]
    data_by_temp = [data[data["temperature"] == temp]['pae_interaction'].values for temp in temperatures]

    plt.figure(figsize=(8, 6))
    plt.boxplot(data_by_temp)

    plt.xticks(range(1, len(temperatures) + 1), temperatures)
    # Add labels and title
    plt.xlabel("-log(Temperature)")
    plt.ylabel("PAE Interaction")
    plt.title("PAE Interaction by Temperature")

    plt.show()
    return

def analyzeMedians(dataFile):
    data = pd.read_csv(dataFile)  # Ensure dataFile is defined elsewhere

    # Process data
    temperatures = data["temperature"].unique()
    temperatures = np.sort(temperatures)[::-1]  # Sort temperatures in descending order

    # Extract median PAE interaction values for each temperature
    data_by_temp = [data[data["temperature"] == temp]['pae_interaction'].values for temp in temperatures]
    medians = [np.median(val) for val in data_by_temp]

    # Plot the data
    plt.plot(temperatures, medians, marker='o', linestyle='None')
    plt.xlabel("-log(Temperature)")
    plt.ylabel("Median PAE Interaction")
    plt.title("Median PAE Interaction by Temperature")
    plt.gca().invert_xaxis()  # Reverse x-axis for descending order
    plt.show()

    normalTemp = np.exp(-1*temperatures)
    plt.plot(normalTemp[0], medians[0], marker='o', color='red', linestyle='None', label='First Point')
    plt.plot(normalTemp[1:], medians[1:], marker='o', linestyle='None')
    plt.xlabel("Temperature")
    plt.ylabel("Median PAE Interaction")
    plt.show()
    return

def firstOrderDecay(x, a, g):
    return a * np.exp(-g * x)

def fitExponential(dataFile):
    data = pd.read_csv(dataFile)
    temperatures = data["temperature"].unique()
    temperatures = np.sort(temperatures)[::-1]
    data_by_temp = [data[data["temperature"] == temp]['pae_interaction'].values for temp in temperatures]

    normalTemp = np.exp(-1*temperatures)
    medians = [np.median(val) for val in data_by_temp]

    try:
        popt, pcov = curve_fit(firstOrderDecay, normalTemp, medians)
        A, gamma = popt
    except RuntimeError as e:
        print(f"Could not fit exponential decay: {e}")
        A, gamma = None, None

# Generate points for the fitted curve if fitting was successful
    if A is not None and gamma is not None:
        x_fit = np.linspace(min(normalTemp), max(normalTemp), 100)  # Generate x values for the fit
        y_fit = firstOrderDecay(x_fit, A, gamma)

        # Plot the original data points
        plt.plot(normalTemp, medians, 'o', label='Data', color='blue')
        plt.plot(normalTemp[0], medians[0], 'o', color='red', label='First Point')  # Highlight first point in red

        # Plot the fitted curve
        plt.plot(x_fit, y_fit, '-', color='green', label=f'Fit: A={A:.3f}, gamma={gamma:.3f}')

        # Add labels and title
        plt.xlabel("Temperatures")
        #plt.gca().invert_xaxis()  # Invert x-axis if needed
        plt.ylabel("Medians")
        plt.title("Exponential Decay Fit to Data")
        plt.legend()

        # Display the plot
        plt.show()

def analyzeLowerQuartile(dataFile):
    data = pd.read_csv(dataFile)  # Ensure dataFile is defined elsewhere

    # Process data
    temperatures = data["temperature"].unique()
    temperatures = np.sort(temperatures)[::-1]  # Sort temperatures in descending order

    # Extract median PAE interaction values for each temperature
    data_by_temp = [data[data["temperature"] == temp]['pae_interaction'].values for temp in temperatures]
    lowerQuartiles = [np.percentile(val, 5) for val in data_by_temp]

    # Plot the data
    plt.plot(temperatures, lowerQuartiles, marker='o', linestyle='None')
    plt.xlabel("-log(Temperature)")
    plt.ylabel("Lower Quartile PAE Interaction")
    plt.title("Lower Quartile PAE Interaction by Temperature")
    plt.gca().invert_xaxis()  # Reverse x-axis for descending order
    plt.show()

    normalTemp = np.exp(-1*temperatures)
    plt.plot(normalTemp[0], lowerQuartiles[0], marker='o', color='red', linestyle='None', label='First Point')
    plt.plot(normalTemp[1:], lowerQuartiles[1:], marker='o')
    plt.xlabel("Temperature")
    plt.ylabel("Lower Quartile PAE Interaction")
    plt.show()
    return

def anova_kruskal(dataFile):
    data = pd.read_csv(dataFile)
    t_groups = [group for name, group in data.groupby('temperature')['pae_interaction']]
    kruskal_stat, kruskal_p = stats.kruskal(*t_groups)
    print(f'Kruskal-Wallis Test: Statistic={kruskal_stat}, p-value={kruskal_p}')
    return

def bootstrapData(dataFile):
    data = pd.read_csv(dataFile)
    temperatures = data["temperature"].unique()
    temperatures = np.sort(temperatures)[::-1]  # Sort temperatures in descending order
    data_by_temp = [data[data["temperature"] == temp]['pae_interaction'].values for temp in temperatures]

    # Parameters for bootstrapping
    n_iterations = 1000
    n_samples = 30

    # Initialize list to store bootstrapped medians
    bootstrapped_lower25th = []
    bootstrapped_lower5th = []

    # Bootstrap for 25th percentile
    for i in range(n_iterations):
        values = []  # Initialize a list to store the 5th percentiles for this iteration

        for temp_data in data_by_temp:
            # Randomly sample data with replacement for each temperature
            sample = np.random.choice(temp_data, size=n_samples, replace=True)
            # Calculate the 5th percentile of the sampled data and append to the values list
            values.append(np.percentile(sample, 5))  # Calculate the 5th percentile

            # Append the list of 5th percentiles for this iteration to the bootstrapped_lower5th list
            bootstrapped_lower25th.append(values)

    # Convert bootstrapped_lower5th to a DataFrame for easier analysis
    bootstrapped_lower25th_df = pd.DataFrame(bootstrapped_lower25th, columns=temperatures)

    # Calculate the mean of the lower 5th percentiles for each temperature
    mean_lower25th = np.mean(bootstrapped_lower25th_df, axis=0)

    # Calculate 95% confidence intervals for each temperature
    confidence_intervals = np.percentile(bootstrapped_lower25th_df, [2.5, 97.5], axis=0)
    
    upper_errors = confidence_intervals[1] - mean_lower25th  # Upper bound - mean
    lower_errors = mean_lower25th - confidence_intervals[0]  # Mean - lower bound

    # Plot the data
    plt.errorbar(temperatures, values, yerr=np.abs(confidence_intervals - values), fmt='o')
    plt.xlabel("-log(Temperature)")
    plt.ylabel("Lower 25th Percentile PAE Interaction")
    plt.title("Lower 25th Percentile PAE Interaction by Temperature with 95% Confidence Intervals")
    plt.gca().invert_xaxis()  # Reverse x-axis for descending order
    plt.show()
    
    for i in range(n_iterations):
        values = []  # Initialize a list to store the 5th percentiles for this iteration

        for temp_data in data_by_temp:
            # Randomly sample data with replacement for each temperature
            sample = np.random.choice(temp_data, size=n_samples, replace=True)
            # Calculate the 5th percentile of the sampled data and append to the values list
            values.append(np.percentile(sample, 5))  # Calculate the 5th percentile

            # Append the list of 5th percentiles for this iteration to the bootstrapped_lower5th list
            bootstrapped_lower5th.append(values)

    # Convert bootstrapped_lower5th to a DataFrame for easier analysis
    bootstrapped_lower5th_df = pd.DataFrame(bootstrapped_lower5th, columns=temperatures)

    # Calculate the mean of the lower 5th percentiles for each temperature
    mean_lower5th = np.mean(bootstrapped_lower5th_df, axis=0)

    # Calculate 95% confidence intervals for each temperature
    confidence_intervals = np.percentile(bootstrapped_lower5th_df, [16.5, 83.5], axis=0)
    
    upper_errors = confidence_intervals[1] - mean_lower5th  # Upper bound - mean
    lower_errors = mean_lower5th - confidence_intervals[0]  # Mean - lower bound

# Plotting the lower 5th percentile values with error bars
    plt.errorbar(temperatures, mean_lower5th, 
             yerr=[lower_errors, upper_errors], 
             fmt='o', capsize=5, label='Mean Lower 5th Percentile')
    plt.xlabel("-log(Temperature)")
    plt.ylabel("Lower 5th Percentile PAE Interaction")
    plt.title("Lower 5th Percentile PAE Interaction by Temperature")
    plt.gca().invert_xaxis()  # Reverse x-axis for descending order
    plt.legend()
    plt.show()

###########################################
# Function Calls and Main Code
###########################################

# Define Parent Directory 
parentDirectory=""

sc_directory = os.path.join(parentDirectory,"experiment8_af2Scores") # Change to directory with score files
csv_name = "tempExp8Scores.csv" # Change to desired output CSV name

# Loop through each file in the directory, not necessary if you already have an AF2 score CSV file
for file in os.listdir(sc_directory):
    print(file)
    filePath = os.path.join(sc_directory, file)
    with open(filePath, 'r') as infile:
        lines = infile.readlines()
    writeScoreCSV(lines, outCSV=csv_name, filename=file)
  

#makeViolinPlot(csv_name)
makeBoxPlot(csv_name)
analyzeMedians(csv_name)
#fitExponential(csv_name)
analyzeLowerQuartile(csv_name)
bootstrapData(csv_name)
#anova_kruskal(csv_name)