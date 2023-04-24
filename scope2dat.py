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
 
def channel_defs(scpchan):
    # Convert the Pandas Series to a string
    scpchan_str = scpchan.iloc[0]

    # Define the wanted strings in lowercase
    pre_strings = ["pre"]
    post_strings = ["post"]
    bottle_strings = ["bottle"]
    trigger_strings = ["trigger", "trig"]

    # Convert the input string to lowercase
    scpchan_lower = scpchan_str.lower()

    if any(s in scpchan_lower for s in pre_strings):
        chdef = 1000
    elif any(s in scpchan_lower for s in post_strings):
        chdef = 667
    elif any(s in scpchan_lower for s in bottle_strings):
        chdef = 5000
    elif any(s in scpchan_lower for s in trigger_strings):
        chdef = 750
    else:
        print("Incorrect column definition in ScopeChannels.csv. Aborting data processing.")
        sys.exit(1)

    return chdef

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
#                                        Reading in scope channels                                 #
####################################################################################################

#Saving the strings from ScopeChannels.csv
channels = read_csv('ScopeChannels.csv')
shot_row = channels.loc[channels['ShotNumber'] == int(shot_num)]
scp2ch1  = shot_row['scp2ch1'] 
scp2ch2  = shot_row['scp2ch2']
scp2ch3  = shot_row['scp2ch3']

ch1def   = channel_defs(scp2ch1)
ch2def   = channel_defs(scp2ch2)
ch3def   = channel_defs(scp2ch3)

####################################################################################################
#                                        Converting voltage to PSI                                 #
####################################################################################################

CH1 = v_to_psi(CH1,ch1def) #Blue line, post-choke
CH2 = v_to_psi(CH2,ch2def) #Red line, pre-choke
CH3 = v_to_psi(CH3,ch3def) #Trigger

# CH1 = v_to_psi(CH1,667) #Blue line, post-choke
# CH2 = v_to_psi(CH2,1000) #Red line, pre-choke

####################################################################################################
#                                       Saving pressure data to CSV                                #
####################################################################################################


#Creating array for new csv file
scope2 = DataFrame({"time2":time2,"BluePost":CH1,"RedPre":CH2,"TRIG":CH3})
scope2 = scope2.drop(index=0) #dropping the units row
scope2 = scope2.reset_index(drop=True)

#Saving to .csv
scope2.to_csv("scope2shot"+shot_num+"_pressure.csv",index=False)

