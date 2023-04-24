# importing module
from pandas import *
import numpy as np
import csv
import sys
import os

########## User-defined functions #############

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
 

####################################################################################################
#                                           Reading CSV file                                       #
####################################################################################################


shot_num = input("Enter shot number to post-process: ")
filename = "shot"+ shot_num +"scp2_raw.csv"
data = read_csv(filename)




####################################################################################################
#                                           Creating arrays                                        #
####################################################################################################

#creating arrays
time2  = data['X'].tolist()
CH1   = data['CH1'].tolist()
CH2   = data['CH2'].tolist()
CH3   = data['CH3'].tolist()
START = data.filter(regex='(?i)^start$', axis=1).squeeze().tolist()
START = START[0]
dt    = data.filter(regex='(?i)^increment$', axis=1).squeeze().tolist()
dt    = dt[0]

#Creating time array
time2 = time_array(time2,START,dt)
data['X'] = time2

####################################################################################################
#                                        Reformatting data frame                                   #
####################################################################################################


#Dropping the first row below headers (units), and the last two columns and saving modified .csv

data = data.drop(index=0) #dropping the units row
data = data.iloc[:, :-2] #Dropping the last two columns
data = data.reset_index(drop=True)
data.to_csv("shot"+ shot_num +"scp2_volts.csv",index=False)

####################################################################################################
#                                        Converting voltage to PSI                                 #
####################################################################################################

CH1 = v_to_psi(CH1,667) #Blue line, post-choke
CH2 = v_to_psi(CH2,1000) #Red line, pre-choke

####################################################################################################
#                                       Saving pressure data to CSV                                #
####################################################################################################


#Creating array for new csv file
scope2 = DataFrame({"time2":time2,"BluePost":CH1,"RedPre":CH2,"TRIG":CH3})
scope2 = scope2.drop(index=0) #dropping the units row
scope2 = scope2.reset_index(drop=True)

#Saving to .csv
scope2.to_csv("scope2shot"+shot_num+"_pressure.csv",index=False)

