# importing module
from pandas import *
import matplotlib.pyplot as plt
import subprocess

shot_num = input("Enter shot number to post-process: ")

subprocess.run(["python3",'scope1dat.py',shot_num])
subprocess.run(["python3",'scope2dat.py',shot_num])


scope1_name = "scope1shot"+ shot_num +"_pressure.csv"
scope2_name = "scope2shot"+ shot_num +"_pressure.csv"

#Opening scope csv files
scope1 = read_csv(scope1_name)
scope2 = read_csv(scope2_name)

#Creating all data arrays
print('Pulling arrays from scope 1 data.')
time1 = scope1['time1'].tolist()
BlueBottle = scope1['BlueBottle'].tolist()
RedBottle = scope1['RedBottle'].tolist()
BluePre = scope1['BluePre'].tolist()
TRIG1 = scope1['TRIG'].tolist()

print('Pulling arrays from scope 2 data.')
time2 = scope2['time2'].tolist()
BluePost = scope2['BluePost'].tolist()
RedPre = scope2['RedPre'].tolist()
TRIG2  = scope2['TRIG'].tolist()

plt.figure(1)
plt.title('Oxygen line pressures')
plt.plot(time1,BlueBottle,time1,BluePre,time2,BluePost)
plt.xlabel("Time (s)")
plt.ylabel("Pressure (PSI)")
plt.legend(["Bottle","Pre-choke","Post-choke"], loc ="lower right")
plt.ylim(0,1000)
print("Saving oxygen line figure as shot_" + shot_num +"_ox_line.svg")
plt.savefig("shot_" + shot_num + "_ox_line.svg")
plt.show()

plt.figure(2)
plt.title('Ethylene line pressures')
plt.plot(time1,RedBottle,time2,RedPre)
plt.xlabel("Time (s)")
plt.ylabel("Pressure (PSI)")
plt.legend(["Bottle","Pre-choke"], loc ="lower right")
plt.ylim(0,1000)
print("Saving fuel line figure as shot_" + shot_num + "_fuel_line.svg")
plt.savefig("shot_" + shot_num + "_fuel_line.svg")
plt.show()
