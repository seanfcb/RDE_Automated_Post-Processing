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
filename = "shot"+ shot_num +"scp1_raw.csv"
data = read_csv(filename)




####################################################################################################
#                                           Creating arrays                                        #
####################################################################################################

#creating arrays
time1 = data['X'].tolist()
CH1   = data['CH1'].tolist()
CH2   = data['CH2'].tolist()
CH3   = data['CH3'].tolist()
CH4   = data['CH4'].tolist()
START = data.filter(regex='(?i)^start$', axis=1).squeeze().tolist()
START = START[0]
dt    = data.filter(regex='(?i)^increment$', axis=1).squeeze().tolist()
dt    = dt[0]

#Creating time array
time1 = time_array(time1,START,dt)
data['X'] = time1

####################################################################################################
#                                        Reformatting data frame                                   #
####################################################################################################


#Dropping the first row below headers (units), and the last two columns and saving modified .csv

data = data.drop(index=0) #dropping the units row
data = data.iloc[:, :-2] #Dropping the last two columns
data = data.reset_index(drop=True)
data.to_csv("shot"+ shot_num +"scp1_volts.csv",index=False)


####################################################################################################
#                                        Reading in scope channels                                 #
####################################################################################################

#Saving the strings from ScopeChannels.csv
channels = read_csv('ScopeChannels.csv')
shot_row = channels.loc[channels['ShotNumber'] == int(shot_num)]
scp1ch1  = shot_row['scp1ch1'] 
scp1ch2  = shot_row['scp1ch2']
scp1ch3  = shot_row['scp1ch3']
scp1ch4  = shot_row['scp1ch4']

ch1def   = channel_defs(scp1ch1)
print('Channel 1 is ' + scp1ch1 + 'psi')
ch2def   = channel_defs(scp1ch2)
print('Channel 2 is ' + scp1ch2 + 'psi')
ch3def   = channel_defs(scp1ch3)
print('Channel 3 is ' + scp1ch3 + 'psi')
ch4def   = channel_defs(scp1ch4)
print('Channel 4 is ' + scp1ch4 + 'psi')

####################################################################################################
#                                        Converting voltage to PSI                                 #
####################################################################################################

CH1 = v_to_psi(CH1,ch1def) #Blue bottle
CH2 = v_to_psi(CH2,ch2def) #Red bottle
CH3 = v_to_psi(CH3,ch3def) #Blue line, pre-choke
CH4 = v_to_psi(CH4,ch4def) #Trigger

# CH1 = v_to_psi(CH1,5000) #Blue bottle
# CH2 = v_to_psi(CH2,5000) #Red bottle
# CH3 = v_to_psi(CH3,1000) #Blue line, pre-choke

####################################################################################################
#                                       Saving pressure data to CSV                                #
####################################################################################################


#Creating array for new csv file
scope1 = DataFrame({"time1":time1,"BlueBottle":CH1,"RedBottle":CH2,"BluePre":CH3,"TRIG":CH4})
scope1 = scope1.drop(index=0) #dropping the units row
scope1 = scope1.reset_index(drop=True)
#Saving to .csv
scope1.to_csv("scope1shot"+shot_num+"_pressure.csv",index=False)

