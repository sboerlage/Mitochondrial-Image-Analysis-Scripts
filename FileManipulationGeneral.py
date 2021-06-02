# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 11:15:51 2016

@author: Sophie
"""

import pandas as pd
import os
import sys
from distutils.util import strtobool

# Implement user yes/no query

def query_yes_no(question):
    sys.stdout.write('%s [y/n]\n' % question)
    while True:
        try:
            return strtobool(input())
        except ValueError:
            sys.stdout.write('Please respond with \'y\' or \'n\'.\n')
            

# Prompt user to enter directory and check the directory to see if it exists and is of the proper structure         
            
found = False

while not found:
    directory = input('Enter directory: ') + '\\'
    if not os.path.isdir(directory):
        print('This directory can not been found. Please enter correct directory.')
    else:
        found = True
 
# Treatments contains the name of every subdirectory in the directory entered besides Final Analysis

treatments = os.listdir(directory)
if os.path.isdir(directory + "\\Final Analysis"):
    treatments.remove('Final Analysis')

# Check to ensure entered directory only contains other directories, exclude Final Analysis folder that results from running the program
       
for subdir in treatments:
    if not os.path.isdir(directory + subdir):
        print('The directory you enter must only contain subdirectories for each different condition.  Please remove any other files or subdirectories from this directory.')
        sys.exit()
        
# Check to ensure 'Analysis' folder exists in each condition subdirectory, exclude Final Analysis folder that results from running the program

for subdir in treatments:
    if not os.path.isdir(directory + subdir + "\\Analysis"):
        print('The condition subdirectory you enter must contain an Analysis folder containing the analysis output of the Fiji program.  Please ensure the Fiji analysis pieline has been run on the data and the Analysis folder is located at ' + directory + subdir)
        sys.exit()

# Check to ensure 'Analysis' subdirectory contains only other directories

for subdir in treatments:
    for file in os.listdir(directory + subdir + "\\Analysis"):
        if not os.path.isdir(directory + subdir + "\\Analysis\\" + file):
            print('The Analysis folder in the condition subdirectory you enter must only contain subdirectories for each different image.  Please remove any other files or subdirectories from the Analysis folder.')
            sys.exit()        
 

name = input('Enter experiment ID or name: ')           

# Query user to find what types of analysis they are using
          
morphology = query_yes_no('Do your image analysis output files contain a morphology summary?')
TMRE = query_yes_no('Do your image analysis output files contain a TMRE summary?')
MTG = query_yes_no('Do your image analysis output files contain a MTG summary?')
branch = query_yes_no('Do your image analysis output files contain a branch summary?')

# Output message and leave program if user needs a type of analysis not contained here

if not morphology and not TMRE and not MTG and not branch:
    print('Then there\'s nothing to analyse! To analyse different features you\'ll have to edit the code. Email Sophie at sophie.boerlage@gmail.com if you have any questions.')
    sys.exit()

# Initialize initialSummary and fullSummarry

initialSummary = pd.DataFrame()
fullSummary = pd.DataFrame(['init'])
    
# loop over every subdirectory in treatments (excludes Analysis Summariees)

for subdir in treatments:    
    
    header = True
    
    # Initialize summary
    
    if not os.path.isdir(directory + subdir + "\\Summary\\"):
        os.makedirs(directory + subdir + "\\Summary\\")
    initialSummary.to_csv(directory + subdir + "\\Summary\\" + subdir + " Master Summary " + name + ".csv", index=False, header=False)      
    
    for file in os.listdir(directory + subdir + "\\Analysis"):
        
        # Read in csv files, exit program and output message if the file cannot be found
        
        if morphology:
            if not os.path.isfile(directory + subdir + "\\Analysis\\" + file + "\\Morphology Summary.csv"):
                print('The file Morphology Summary.csv cannot be found at ' + directory + subdir + "\\Analysis\\" + file + '. Please ensure that the morphology summary exists and that the file is named Morphology Summary.csv then re-run the program')
                sys.exit()
            else:
                morphologySummary = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\Morphology Summary.csv")
                
        if MTG:
            if not os.path.isfile(directory + subdir + "\\Analysis\\" + file + "\\MTG Summary.csv"):
                print('The file MTG Summary.csv cannot be found at ' + directory + subdir + "\\Analysis\\" + file + '. Please ensure that the MTG summary exists and that the file is named MTG Summary.csv then re-run the program')
                sys.exit()
            else:
                MTGSummary = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\MTG Summary.csv")
                MTGSummary.columns = [' ', 'MTG']

        if TMRE:
            if not os.path.isfile(directory + subdir + "\\Analysis\\" + file + "\\TMRE Summary.csv"):
                print('The file TMRE Summary.csv cannot be found at ' + directory + subdir + "\\Analysis\\" + file + '. Please ensure that the TMRE summary exists and that the file is named TMRE Summary.csv then re-run the program')
                sys.exit()
            else:
                TMRESummary = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\TMRE Summary.csv")
                TMRESummary.columns = [' ', 'TMRE']

        if branch:
            if not os.path.isfile(directory + subdir + "\\Analysis\\" + file + "\\Skeleton Summary.csv"):
                print('The file Skeleton Summary.csv cannot be found at ' + directory + subdir + "\\Analysis\\" + file + '. Please ensure that the branching summary exists and that the file is named Skeleton Summary.csv then re-run the program')
                sys.exit()
            else:
                branchSummary = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\Skeleton Summary.csv")
                
        # Select and do operations on the data we're interested in        
                
        if morphology:
            morphologyAverages = morphologySummary.mean()
            formFactor = 1/morphologySummary['Circ.'] 
            formFactorSeries = pd.Series(formFactor.mean(), index=['Form Factor'])
            sumSeries = morphologySummary.sum()
            totalAreaSeries = pd.Series(sumSeries['Area'], index=['Total Area'])
            
        if TMRE:
            TMREAverage = TMRESummary.mean()
            
        if MTG:
            MTGAverage = MTGSummary.mean()
            
        if TMRE and MTG:
            ratioTMRE_MTG = TMRESummary['TMRE']/MTGSummary['MTG']
            ratioTMRE_MTGAverage = pd.Series(ratioTMRE_MTG.mean(), index=['Ratio'])
            ratioSummary = pd.DataFrame({'TMRE' : pd.Series(TMRESummary['TMRE']), 'MTG' : pd.Series(MTGSummary['MTG']), 'Ratio' : pd.Series(ratioTMRE_MTG)})
            reorderCols = ['TMRE', 'MTG', 'Ratio']
            ratioSummary = ratioSummary[reorderCols]
            ratioSummary.to_csv(directory + subdir + "\\Analysis\\" + file + "\\Ratio Summary.csv", index=False)
        
        if branch:
            branchSummary = branchSummary.transpose()
            
        # There will be an index and a count column independent of which type of data is analysed
            
        indexSeries = pd.Series([file], index=['Index'])
                
        if morphology:
            countSeries = pd.Series(len(morphologySummary), index=['Count'])
        elif TMRE:
            countSeries = pd.Series(len(TMRESummary), index=['Count'])
        elif MTG:
            countSeries = pd.Series(len(MTGSummary), index=['Count'])
        elif branch:
            countSeries = pd.Series(branchSummary[1:2], index=['Count'])
        
        # Add all relevant series to a final data summary
            
        summarySeries = indexSeries.append(countSeries)
        
        if morphology:
            summarySeries = summarySeries.append(morphologyAverages[1:9])
            summarySeries = summarySeries.append(formFactorSeries)
            summarySeries = summarySeries.append(totalAreaSeries)
        
        if TMRE:
            summarySeries = summarySeries.append(TMREAverage[1:2])
        
        if MTG:
            summarySeries = summarySeries.append(MTGAverage[1:2])
       
        if TMRE and MTG:
            summarySeries = summarySeries.append(ratioTMRE_MTGAverage)
            
        if branch:
            summarySeries = summarySeries.append(branchSummary[2:8])
            
        summaryDataFrame = pd.DataFrame(summarySeries)
        summaryDataTransposed = summaryDataFrame.transpose()
              
        # Save the data line by line to the mastre summary csv file.  Include the header with the first line only
        
        if header:
            with open(directory + subdir + "\\Summary\\" + subdir + " Master Summary " + name + ".csv", 'a') as f:
                summaryDataTransposed.to_csv(f, index=False)
                f.close()
        else:
            with open(directory + subdir + "\\Summary\\" + subdir + " Master Summary " + name + ".csv", 'a') as f:
                summaryDataTransposed.to_csv(f, index=False, header=False)
                f.close()
        
        header = False
        
    # Read in the data from each condition 
        
    data = pd.read_csv(directory + subdir + "\\Summary\\" + subdir + " Master Summary " + name + ".csv")
    
    # Add the conditions to the first row of each data summary, then add the data for each condition to the fullSummary
        
    conditions = pd.DataFrame([subdir] * len(data.columns))
    conditions = conditions.transpose()
    conditions.columns = data.columns
    conditionSummary = conditions.append(data, ignore_index=True)
    fullSummary = pd.concat([fullSummary, conditionSummary], axis=1)    

# Create subdirectory for all further analysis, and output the final summary to this location

if not os.path.isdir(directory + "\\Final Analysis"):
    os.makedirs(directory + "\\Final Analysis")

del fullSummary[0]
fullSummary.to_csv(directory + "\\Final Analysis\\Summary " + name + ".csv", index=False)

# Create seperate csv files for each parameter to facilitate copy + pasting into GraphPad or a similar analysis or graphing program

for parameter in conditionSummary.columns:
    parameterSummary = fullSummary[parameter]
    parameterSummary.to_csv(directory + "\\Final Analysis\\" + parameter + " " + name + ".csv", index=False)

