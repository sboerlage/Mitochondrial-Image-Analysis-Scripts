# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 14:23:46 2016

@author: Sophie Boerlage
"""

import pandas as pd
import os

directory = "C:\\Users\\Norsys\\Desktop\\Test\\"

fullSummary = pd.DataFrame(['init'])

for subdir in os.listdir(directory):
    os.makedirs(directory + subdir + "\\Test\\")
    for file in os.listdir(directory + subdir + "\\Analysis"):
        
        morphologySummary = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\Morphology Summary.csv", header=None)
        MTGSummary = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\MTG Summary.csv", header=None)
        
        morphologySummary = morphologySummary.drop(morphologySummary.columns[[0]], axis=1)
        MTGSummary = MTGSummary.drop(MTGSummary.columns[[0]], axis=1)
        
        averageArea = morphologySummary[1]
        averageMTG = MTGSummary[1]
               
        dataSummary = pd.concat([averageArea, MTGSummary], axis=1, ignore_index=True)
        
        #dataSummary = dataSummary.drop(dataSummary.???[[0]], axis=0)
        
        with open(directory + subdir + "\\Test\\Master Summary.csv", 'a') as f:
                dataSummary.to_csv(f, header=False)
                f.close()
    
    data = pd.read_csv(directory + subdir + "\\Test\\Master Summary.csv")
    fullSummary = pd.concat([fullSummary, data], axis=0, ignore_index=True)
    
os.makedirs(directory + "\\Test")
del fullSummary[0]
fullSummary.to_csv(directory + "\\Test\\Summary.csv", index=False, header=False)



