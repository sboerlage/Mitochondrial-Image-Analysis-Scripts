# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 15:43:35 2016

@author: Sophie Boerlage
"""

import pandas as pd
import os

#Use directory where images are stored

directory = "C:\\Users\\Norsys\\Desktop\\PythonTest\\"

    
for subdir in os.listdir(directory):
        for file in os.listdir(directory + subdir + "\\Analysis"):
            MS = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\Morphology Summary.csv")
            MTG = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\MTG Summary.csv")
            TMRE = pd.read_csv(directory + subdir + "\\Analysis\\" + file + "\\TMRE Summary.csv")
            
            initmerged = MS.merge(MTG, on=' ')
            merged = initmerged.merge(TMRE, on=' ')

            merged.columns = ['Num','Area','Perim.','Circ.','AR','Round','Solidity','MTG','TMRE']

            merged.to_csv(directory + subdir + "\\Analysis\\" + file + "\\Summary.csv", index=False)