# importing module
from pandas import *
import matplotlib.pyplot as plt

def v_to_psi(CH,psi):
	i = 0
	for j in CH:
		j = (j-0.5)/4*psi
		CH[i] = j
		i=i+1
	return CH
def time_array(time,START,dt):
	for i in time:
		if i == 0:
			time[i]=START
		else:
			time[i] = time[i-1]+dt
	return time
 
# reading CSV file
data = read_csv("shot122scp2.csv")

#creating arrays
time2  = data['X'].tolist()
CH1   = data['CH1'].tolist()
CH2   = data['CH2'].tolist()
CH3   = data['CH3'].tolist()
START = data['START'].tolist()
START = START[0]
dt    = data['INCREMENT'].tolist()
dt    = dt[0]

#Creating time array
time2 = time_array(time2,START,dt)

#Voltage to PSI
CH1 = v_to_psi(CH1,667) #Blue line, post-choke
CH2 = v_to_psi(CH2,1000) #Red line, pre-choke

#Creating array for new csv file
scope2 = DataFrame({"time2":time2,"BluePost":CH1,"RedPre":CH2,"TRIG":CH3})

#Saving to .csv
scope2.to_csv("scope2.csv",index=False)

