#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sys
import argparse

def check_temp(warn, crit, adapter):
    """ 
    This is a simple Nagios plugin to
    check the temperature with lm-sensors and then
    returning the correct return code to main.
    """ 

    # Use lm-sensors to check the temperature
    try:
        sensors_output = subprocess.check_output(['sensors'])
    except OSError:
        print "Couldn't execute sensors (from lm-sensors)"
        sys.exit(3)

    # Grab the temperature for the specified adapter by splitting the string
    # into a list and then getting the index number for the adapter name and
    # adding 5 to the index number.
    # Lastly, we strip away the + sign and the degree symbols and typecast it
    # to a float
    sensors_output = sensors_output.split()
    t = sensors_output.index(adapter) + 5
    temp = sensors_output[t]
    temp = temp[1:-3]
    temp = float(temp)
    
    if warn > crit:
        print "Warning temp must be less than critical temp"
        sys.exit(3)

    # Do the actual temperature check/comparison.
    # For each case we return both the code and the current temperature
    if temp < warn:
        return 0, temp

    elif temp > warn and temp < crit:
        return 1, temp

    elif temp >= crit:
        return 2, temp

    else:
        return 3, temp
        

def main():
    
    # Parse command line options with argparse
    cli_parser = argparse.ArgumentParser() 
    cli_parser.add_argument('-w', metavar='N', type=float, required=True,
        help='warning temperature')
    cli_parser.add_argument('-c', metavar='N', type=float, required=True,
        help='critical temperature')
    cli_parser.add_argument('-a', metavar='string', type=str, required=True,
        help='the adapter to monitor (for example: acpitz-virtual-0)')
    args = cli_parser.parse_args()

    # Get the return-code and temperature from check_temp function
    return_code, temp = (check_temp(args.w, args.c, args.a)) 
    
    # Print temperature and message and then exit with the correct return code
    if return_code == 0:
        print ("OK - Temperature is " + str(temp))
        sys.exit(0)
    elif return_code == 1:
        print ("WARNING - Temperature is " + str(temp))
        sys.exit(1)
    elif return_code == 2:
        print ("CRITICAL - Temperature is " + str(temp))
        sys.exit(2)
    else:
        print ("UNKNOWN - Something went wrong with " + sys.argv[0] + "!")
        sys.exit(3)
        
if __name__=='__main__':
    main()
