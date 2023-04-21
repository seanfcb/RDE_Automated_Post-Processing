# importing module
from pandas import *
import numpy as np
import csv
import sys
import os

# def v_to_psi(CH,psi):
# 	i = 0
# 	for j in CH:
# 		j = (j-0.5)/4*psi
# 		CH[i] = j
# 		i=i+1
# 	return CH

def v_to_psi(CH, psi):
    for i, x in enumerate(CH[1:], start=1):
        CH[i] = (float(x) - 0.5) / 4 * psi
    return CH

def time_array(time,START,dt):
	for i in range(1,len(time)):
		if i == 1:
			time[i]=START
		else:
			time[i] = time[i-1]+dt
	return time
 
# reading CSV file

shot_num = input("Enter shot number to post-process: ")
filename = "shot"+ shot_num +"scp1_raw.csv"
data = read_csv(filename)


#creating arrays
time1 = data['X'].tolist()
CH1   = data['CH1'].tolist()
CH2   = data['CH2'].tolist()
CH3   = data['CH3'].tolist()
CH4   = data['CH4'].tolist()
#START = data['START'].tolist()
START = data.filter(regex='(?i)^start$', axis=1).squeeze().tolist()
START = START[0]
#dt    = data['INCREMENT'].tolist()
dt    = data.filter(regex='(?i)^increment$', axis=1).squeeze().tolist()
dt    = dt[0]

#Creating time array
time1 = time_array(time1,START,dt)

#Dropping the first row below headers (units), and the last two columns and saving modified .csv

data = data.drop(index=0) #dropping the units row
data = data.iloc[:, :-2] #Dropping the last two columns
data = data.reset_index(drop=True)
data.to_csv("shot"+ shot_num +"scp1.csv",index=False)


#Voltage to PSI
CH1 = v_to_psi(CH1,5000) #Blue bottle
CH2 = v_to_psi(CH2,5000) #Red bottle
CH3 = v_to_psi(CH3,1000) #Blue line, pre-choke

#Creating array for new csv file
scope1 = DataFrame({"time1":time1,"BlueBottle":CH1,"RedBottle":CH2,"BluePre":CH3,"TRIG":CH4})

#Saving to .csv
scope1.to_csv("scope1shot"+shot_num+"_pressure.csv",index=False)

