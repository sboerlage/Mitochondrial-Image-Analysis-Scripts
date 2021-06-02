# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 15:44:38 2016

@author: Sophie Boerlage
"""
import pandas as pd
import os

# Directory must be set up with a different file for each imaging condition and all the images for that condition contained within their files
# Currently, any different directry structure will not work, so the directory must not contain any other file types

directory = "C:\\Users\\Norsys\\Desktop\\PythonTest\\"

# Loop over the files of different image conditions

for subdir in os.listdir(directory):

        # Initialize the csv file that will be used as the Master Summary   
        '''
        header = pd.DataFrame(['Count','Area','Perim.','Circ.','AR','Round','Solidity','MTG','TMRE','Ratio','FormFactor'])
        tranHeader = header.transpose()
        tranHeader.to_csv(directory + subdir + "\\Analysis\\Master Summary.csv", index=False)     
        '''
        # Loop over all the images within each image condition file
        
        for file in os.listdir(directory + subdir + "\\Analysis"):
            data = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\Summary.csv")
                    
            # Take the        add the form factor, 1/circularity            
                    
            average = data.mean()
            TMRE_MTGRatio = pd.Series((average[8]/average[7]), index=["Ratio"])
            FFSeries = pd.Series(1/average[4])
            countSeries = pd.Series(len(data), index=["Count"])
            avgSeries = countSeries.append(average[1:9])
            ratioSeries = avgSeries.append(TMRE_MTGRatio)
            finSeries = ratioSeries.append(FFSeries)
            
            df = pd.DataFrame(finSeries)
            tdf = df.transpose()

            with open(directory + subdir + "\\Analysis\\Master Summary.csv", 'a') as f:
                tdf.to_csv(f, header=False, index=False)
                f.close()
                
       # with open(directory + subdir + "\\Analysis\\Master Summary.csv", 'a') as f:
