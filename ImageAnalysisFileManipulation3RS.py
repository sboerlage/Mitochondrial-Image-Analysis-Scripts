# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 16:05:39 2016

@author: Sophie Boerlage
"""

'''
To use the program files must be in the following particular structure:
Subdirectories named after the conditions in a directory entered into the directory variable
Each subdirectory must contain a folder named "Analysis" that contains folders for each image
Each image folder must contain three csv files, which contain the Morphology Summary, MTG Summary,
and TMRE Summary, with those names
There can be no other files within the directory, the analysis folder or the image folders, but the 
condition folders may contain any othe files

This file structure can be obtained by running the "Altered TMRE Analysis Pipeline" on images contained 
within the condition subdirectories

'''
import pandas as pd
import os

# Directory where condition subdirectories containing images and Analysis folder are stored

directory = "C:\\Users\\Sophie\\Desktop\\Min6\\"

# Specify the name of the experiment to be the title of the summary sheets

name = "Live DMSO"
    
'''
Ask for user input

directory = input("Directory name must conain double backslashes and backslashes at the end.  Enter directory: ")

name = input("Enter name: ")

'''

# Specify order for data to be presented in GraphPad, based on the alphabetical order of the conditions in the directory, indexed from 0

conditionOrder = [3, 2, 1, 0]



# Initialize fullSummarry

fullSummary = pd.DataFrame(['init'])
    
for subdir in os.listdir(directory):
        
        # Initialize the Master Summary for each condition by specifying the column names with the condtion and the value measured
        # and save the file with the headers in the condition subdirectory
        # The average data from each image will be added to this file one line at a time
        # The header conditions are specific to the Fiji program and should be changed if the Fiji analysis changes
        
        header = pd.DataFrame(['0','Index','Count','Area','Perim.','Circ.','AR','Round','Solidity','FormFactor','TotalArea','Branches','Branch Length','Branch Points','Branches per Mito','Branch Length per Mito','Branch Points per Mito'])
        header = header.transpose()
        conditions = pd.DataFrame(['0',subdir,subdir,subdir,subdir,subdir,subdir,subdir,subdir,subdir,subdir,subdir,subdir,subdir,subdir,subdir,subdir])
        conditions = conditions.transpose()
        initialSummary = pd.concat([conditions,header], axis=0)
        os.makedirs(directory + subdir + "\\Summary\\")
        initialSummary.to_csv(directory + subdir + "\\Summary\\" + subdir + " Master Summary " + name + ".csv", index=False, header=False)
        
        for file in os.listdir(directory + subdir + "\\Analysis"):
              
            # Read in the data from the Fiji output csv files
            
            morphologySummary = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\Morphology Summary.csv")
            #MTGSummary = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\MTG Summary.csv")
            #TMRESummary = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\TMRE Summary.csv")
            branchSummary = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\Skeleton Summary.csv")
            
            # Merge the morphology summary, the MTG summary, and the TMRE summary into dataSummary
            
            #dataSummary = morphologySummary.merge(MTGSummary, on=' ')
            #dataSummary = dataSummary.merge(TMRESummary, on=' ')
            dataSummary = morphologySummary
            # Add columns to dataSummary and output to the directory with the files so a summary for each image is easily accessible
            
            dataSummary.columns = ['Count','Area','Perimeter','Circularity','Aspect Ratio','Round','Solidity']
            dataSummary.to_csv(directory + subdir + "\\Analysis\\" + file + "\\" + file + " Summary.csv", index=False)
                              
            '''
            Calculate any parameters you want to examine using the data
            Average over all the particles in an image
            Calculate the ratio of TMRE/MTG in each image
            Calculate the average of the TMRE/MTG ratios
            Calculate the form factor (1/circularity)
            Count the number of particles
            Calculate the sum of the data (For calculating total area)
            Index the data by the image name
            Add the data form branchSummary
            
            '''
                   
            averages = dataSummary.mean()
            #Ratiovals = dataSummary['TMRE']/dataSummary['MTG']
            #TMRE_MTGRatio = pd.Series(Ratiovals.mean(), index=['Ratio'])
            FFSeries = pd.Series(1/averages[3], index=['Form Factor'])
            countSeries = pd.Series(len(dataSummary), index=['Count'])
            sumSeries = dataSummary.sum()
            indexSeries = pd.Series([file], index=['Index'])
            branchSummary = branchSummary.transpose()
            
            finalSeries = indexSeries.append(countSeries)
            finalSeries = finalSeries.append(averages[1:9])
            #finalSeries = finalSeries.append(TMRE_MTGRatio)
            finalSeries = finalSeries.append(FFSeries)
            finalSeries = finalSeries.append(sumSeries[1:2])
            finalSeries = finalSeries.append(branchSummary[2:8])
            
            imageDataAverages = pd.DataFrame(finalSeries)
            dataAveragesTransposed = imageDataAverages.transpose()

            with open(directory + subdir + "\\Summary\\" + subdir + " Master Summary " + name + ".csv", 'a') as f:
                dataAveragesTransposed.to_csv(f, header=False)
                f.close()
     
        # Open master summary file, add heading

        data = pd.read_csv(directory + subdir + "\\Summary\\" + subdir + " Master Summary " + name + ".csv", header=None)
        fullSummary = pd.concat([fullSummary, data], axis=1)

# Create subdirectory for all further analysis, and output the master summary to this location
     
os.makedirs(directory + "\\Analysis")
del fullSummary[0]
fullSummary.to_csv(directory + "\\Analysis\\Summary " + name + ".csv", index=False, header=False)
     

'''
Create seperate csv files for each parameter to facilitate copy + pasting into GraphPad or a similar analysis 
or graphing program:

Create a dataFrame that contains the four columns that are labeled with the desired parameter using the number 
associated with that parameter

Relabel the column numbers so that you can order the columns based on how they will appear in the graphing program

Use conditionOrder to order the columns based on 

Output the ordered dataFrame to a csv file that incluses the name of the experiment
    -> File will contain the condition name, the parameter, and the data.  To find the image index, refer back to the 
       full summary
'''
'''
count = fullSummary[[2]]
count.columns = [0, 1, 2, 3]
countOrdered = count[conditionOrder]
countOrdered.to_csv(directory + "\\Analysis\\Count " + name + ".csv", index=False, header=False)

area = fullSummary[[3]]
area.columns = [0, 1, 2, 3]
areaOrdered = area[conditionOrder]
areaOrdered.to_csv(directory + "\\Analysis\\Area " + name + ".csv", index=False, header=False)

perimeter = fullSummary[[4]]
perimeter.columns = [0, 1, 2, 3]
perimeterOrdered = perimeter[conditionOrder]
perimeterOrdered.to_csv(directory + "\\Analysis\\Perimeter " + name + ".csv", index=False, header=False)

circularity = fullSummary[[5]]
circularity.columns = [0, 1, 2, 3]
circularityOrdered = circularity[conditionOrder]
circularityOrdered.to_csv(directory + "\\Analysis\\Circularity " + name + ".csv", index=False, header=False)

AR = fullSummary[[6]]
AR.columns = [0, 1, 2, 3]
AROrdered = AR[conditionOrder]
AROrdered.to_csv(directory + "\\Analysis\\Aspect Ratio " + name + ".csv", index=False, header=False)

Round = fullSummary[[7]]
Round.columns = [0, 1, 2, 3]
RoundOrdered = Round[conditionOrder]
RoundOrdered.to_csv(directory + "\\Analysis\\Round " + name + ".csv", index=False, header=False)

# Solidity not used

MTG = fullSummary[[9]]
MTG.columns = [0, 1, 2, 3]
MTGOrdered = MTG[conditionOrder]
MTGOrdered.to_csv(directory + "\\Analysis\\MTG " + name + ".csv", index=False, header=False)

TMRE = fullSummary[[10]]
TMRE.columns = [0, 1, 2, 3]
TMREOrdered = TMRE[conditionOrder]
TMREOrdered.to_csv(directory + "\\Analysis\\TMRE " + name + ".csv", index=False, header=False)

ratioTMRE_MTG = fullSummary[[11]]
ratioTMRE_MTG.columns = [0, 1, 2, 3]
ratioTMRE_MTGOrdered = ratioTMRE_MTG[conditionOrder]
ratioTMRE_MTGOrdered.to_csv(directory + "\\Analysis\\Ratio " + name + ".csv", index=False, header=False)

formFactor = fullSummary[[12]]
formFactor.columns = [0, 1, 2, 3]
formFactorOrdered = formFactor[conditionOrder]
formFactorOrdered.to_csv(directory + "\\Analysis\\Form Factor " + name + ".csv", index=False, header=False)

totalArea = fullSummary[[13]]
totalArea.columns = [0, 1, 2, 3]
totalAreaOrdered = totalArea[conditionOrder]
totalAreaOrdered.to_csv(directory + "\\Analysis\\Total Area " + name + ".csv", index=False, header=False)

branches = fullSummary[[14]]
branches.columns = [0, 1, 2, 3]
branchesOrdered = branches[conditionOrder]
branchesOrdered.to_csv(directory + "\\Analysis\\Branches " + name + ".csv", index=False, header=False)

branchLength = fullSummary[[15]]
branchLength.columns = [0, 1, 2, 3]
branchLengthOrdered = branchLength[conditionOrder]
branchLengthOrdered.to_csv(directory + "\\Analysis\\Branch Length " + name + ".csv", index=False, header=False)

branchPoints = fullSummary[[16]]
branchPoints.columns = [0, 1, 2, 3]
branchPointsOrdered = branchPoints[conditionOrder]
branchPointsOrdered.to_csv(directory + "\\Analysis\\Branch Points " + name + ".csv", index=False, header=False)

mitoBranches = fullSummary[[17]]
mitoBranches.columns = [0, 1, 2, 3]
mitoBranchesOrdered = mitoBranches[conditionOrder]
mitoBranchesOrdered.to_csv(directory + "\\Analysis\\Branches per Mitochondria " + name + ".csv", index=False, header=False)

branchLengthPerMito = fullSummary[[18]]
branchLengthPerMito.columns = [0, 1, 2, 3]
branchLengthPerMitoOrdered = branchLengthPerMito[conditionOrder]
branchLengthPerMitoOrdered.to_csv(directory + "\\Analysis\\Branch Length per Mitochondria " + name + ".csv", index=False, header=False)

branchPointsPerMito = fullSummary[[19]]
branchPointsPerMito.columns = [0, 1, 2, 3]
branchPointsPerMitoOrdered = branchPointsPerMito[conditionOrder]
branchPointsPerMitoOrdered.to_csv(directory + "\\Analysis\\Branch Points per Mitochondria " + name + ".csv", index=False, header=False)
'''