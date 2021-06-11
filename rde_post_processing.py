#!/usr/bin/python
import argparse
import os
import csv
from decimal import *
from collections import namedtuple
from math import sqrt, pi

#############
# Constants #
#############
C2H4_GAMMA = Decimal(1.24)
O2_GAMMA = Decimal(1.4)

C2H4_MM = 28
O2_MM = 32

BOTTLE_TEMPERATURE = 300
FOX_RATIO = Decimal(28 / 124)

##############
# Data Model #
##############

DataPoint = namedtuple('DataPoint', ['voltage', 'psi', 'pa'])
DataLine = namedtuple('DataLine', ['sequence', 'time', 'channel_1', 'channel_2', 'channel_3', 'channel_4'])
Output = namedtuple(
    'Output',
    ['time', 'o2_p', 'o2_po', 'o2_mach', 'o2_flow', 'c2h4_p', 'c2h4_po',
     'c2h4_mach', 'c2h4_flow', 'phi' ]
)



##################
# Math Functions #
##################
def v_to_psi(v, p_range):
    p = ((v - Decimal(0.5)) / Decimal(4)) * p_range
    return p

def mass_flow(po, gamma, mach, Mm):
    D = Decimal(0.277 * 0.0254)
    R = Decimal(8314 / Mm)
    pipe_a = Decimal(Decimal(pi) * Decimal(D ** 2) / 4)
    gamma_1 = Decimal((gamma + 1) / (2 * (gamma-1)))
    gamma_2 = Decimal(1 + ((gamma - 1) / 2) * (mach**2))
    x = gamma/R/BOTTLE_TEMPERATURE
    m_dot = po * pipe_a * Decimal(sqrt(x)) * Decimal(mach / Decimal(gamma_2**gamma_1))
    return m_dot

def mach_number(line_pressure, bottle_pressure, gamma):
    pr = Decimal(bottle_pressure / line_pressure)
    M = Decimal(sqrt((pr ** ((gamma - 1) / gamma) - 1) * 2 / (gamma - 1)))
    return M

def equivalence_ratio(flow_c2h4, flow_o2):
    return (flow_c2h4 / flow_o2) / FOX_RATIO

def psi_to_pa(psi):
    pa = psi * 101325 / Decimal(14.7)
    return pa

##################
# Data functions #
##################
def get_lines(filename):
    with open(filename, 'r') as f:
        for line in f.readlines():
            yield line.split(',') 
        

def transform_voltage_value(dec, p_range):
    # If we have a p_range of 0, it means to NOT transform this voltage value
    if p_range == 0:
        return dec
    psi = v_to_psi(dec, p_range)
    pa = psi_to_pa(psi)
    return DataPoint(dec, psi, pa)

def parse_lines(line_iterator, start, increment, p_ranges):
    for line in line_iterator:
        seq, ch1, ch2, ch3, ch4, _ = line
        time = start + int(seq) * increment
        if time >= 0:
            yield DataLine(
                int(seq),
                time,
                transform_voltage_value(Decimal(ch1), p_ranges[0]),
                transform_voltage_value(Decimal(ch2), p_ranges[1]),
                transform_voltage_value(Decimal(ch3), p_ranges[2]),
                transform_voltage_value(Decimal(ch4), p_ranges[3]),
            )

def get_line_iterator(filename, p_ranges):
    iterator = get_lines(filename)
    header_1 = next(iterator)
    header_2 = next(iterator)
    start_time = Decimal(header_2[5])
    increment = Decimal(header_2[6])
    return parse_lines(iterator, start_time, increment, p_ranges)
    
def merge_lines(line_iterator_1, line_iterator_2):
    try:
        while True:
            l1 = next(line_iterator_1)
            l2 = next(line_iterator_2)
            assert l1.time == l2.time
            if (l2.channel_1.pa / l1.channel_2.pa < 1):
                continue
            if (l2.channel_2.pa / l1.channel_3.pa < 1):
                continue

            mach_o2 = mach_number(l1.channel_2.pa, l2.channel_1.pa, O2_GAMMA)
            flow_o2 = mass_flow(l2.channel_1.pa, O2_GAMMA, mach_o2, O2_MM)
                            
            mach_c2h4 = mach_number(l1.channel_3.pa, l2.channel_2.pa, C2H4_GAMMA)
            flow_c2h4 = mass_flow(l2.channel_2.pa, C2H4_GAMMA, mach_c2h4, C2H4_MM)
            phi = equivalence_ratio(flow_c2h4, flow_o2)

            yield Output(
                l1.time,
                l1.channel_2.psi,
                l2.channel_1.psi,
                mach_o2,
                round(flow_o2 * 1000),
                l1.channel_3.psi,
                l2.channel_2.psi,
                mach_c2h4,
                round(flow_c2h4 * 1000),
                phi,
            )
    except StopIteration:
        print('Lines are merged')
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load two test result files and produce a comibned and computed file')
    parser.add_argument('test', help="The test number (ie SH32)")
    args = parser.parse_args()
    folder = os.getcwd()
    print(f"Looking for files SCP1{args.test}.csv and SCP2{args.test}.csv in {folder}")

    scp_1_ranges = [667, 1000, 1000, 0]
    scp_2_ranges = [5000, 5000, 0, 30]
    lines_1 = get_line_iterator(os.path.join(folder, f"SCP1{args.test}.csv"), scp_1_ranges)
    lines_2 = get_line_iterator(os.path.join(folder, f"SCP2{args.test}.csv"), scp_2_ranges)
    
    lines = list(merge_lines(lines_1, lines_2))
    print(f"Writing file {args.test}.csv")
    with open(f"{args.test}.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(Output._fields)
        for line in lines:
            csvwriter.writerow(line)
