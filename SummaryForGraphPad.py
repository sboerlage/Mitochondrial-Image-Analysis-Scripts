# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 12:30:01 2016

@author: Norsys
"""
import pandas as pd
import os

# Create files that have the data of all conditions for on parameter - ease of copy/paste into graphpad

directory = "C:\\Users\\Norsys\\Desktop\\PythonTest\\"
#conditionNumber = 3
conditionOrder = [2, 3, 0, 1]

init = pd.DataFrame(['init'])

for subdir in os.listdir(directory):
    data = pd.read_csv(directory + subdir + "\\Analysis\\Master Summary.csv")
    init = pd.concat([init, data], axis=1, ignore_index=True, keys=['init', 'subdir'])

os.makedirs(directory + "\\Analysis")
del init[0]
init.to_csv(directory + "\\Analysis\\Summary.csv", index=False)

# Take the columns relating to the named perameter and arrange them in a new file in the order of specified by conditionOrder

count = init[[(conditionOrder[0]*11+1),(conditionOrder[1]*11+1),(conditionOrder[2]*11+1),(conditionOrder[3]*11+1)]]
count.to_csv(directory + "\\Analysis\\Count.csv", index=False)

area = init[[(conditionOrder[0]*11+2),(conditionOrder[1]*11+2),(conditionOrder[2]*11+2),(conditionOrder[3]*11+2)]]
area.to_csv(directory + "\\Analysis\\Area.csv", index=False)

perimeter = init[[(conditionOrder[0]*11+3),(conditionOrder[1]*11+3),(conditionOrder[2]*11+3),(conditionOrder[3]*11+3)]]
perimeter.to_csv(directory + "\\Analysis\\Perimeter.csv", index=False)

circularity = init[[(conditionOrder[0]*11+4),(conditionOrder[1]*11+4),(conditionOrder[2]*11+4),(conditionOrder[3]*11+4)]]
circularity.to_csv(directory + "\\Analysis\\Circularity.csv", index=False)

AR = init[[(conditionOrder[0]*11+5),(conditionOrder[1]*11+5),(conditionOrder[2]*11+5),(conditionOrder[3]*11+5)]]
AR.to_csv(directory + "\\Analysis\\Aspect Ratio.csv", index=False)

Round = init[[(conditionOrder[0]*11+6),(conditionOrder[1]*11+6),(conditionOrder[2]*11+6),(conditionOrder[3]*11+6)]]
Round.to_csv(directory + "\\Analysis\\Round.csv", index=False)

# Solidity not used

MTG = init[[(conditionOrder[0]*11+8),(conditionOrder[1]*11+8),(conditionOrder[2]*11+8),(conditionOrder[3]*11+8)]]
MTG.to_csv(directory + "\\Analysis\\MTG.csv", index=False)

TMRE = init[[(conditionOrder[0]*11+9),(conditionOrder[1]*11+9),(conditionOrder[2]*11+9),(conditionOrder[3]*11+9)]]
TMRE.to_csv(directory + "\\Analysis\\TMRE.csv", index=False)

ratioTMRE_MTG = init[[(conditionOrder[0]*11+10),(conditionOrder[1]*11+10),(conditionOrder[2]*11+10),(conditionOrder[3]*11+10)]]
ratioTMRE_MTG.to_csv(directory + "\\Analysis\\Ratio.csv", index=False)

formFactor = init[[(conditionOrder[0]*11+11),(conditionOrder[1]*11+11),(conditionOrder[2]*11+11),(conditionOrder[3]*11+11)]]
formFactor.to_csv(directory + "\\Analysis\\Form Factor.csv", index=False)
