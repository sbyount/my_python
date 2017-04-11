#!/usr/bin/env python
'''
Script to record pre-change and post-change captures using Netmiko.
User is prompted for two text files, as well at domain password
-First text file contains the CIs: "CHG000xxxx.txt" in the local directory
-Second text file contains the commands to run for the OS of the CI's

Script creates output log file int the following format:
    "CHG000xxxx_CINAME_DATETIME.log"

4/11/17 - Adding multithreading

'''

# Imports
from netmiko import ConnectHandler # Connect to Cisco devices
from getpass import getuser, getpass # Get usernames and passwords
import time
from datetime import datetime # Use for log file stamping, and timing
import threading # for multithreading
import sys # Use system exit message
from os.path import exists # Use to check to see if a file exists
import os # Use to list current folder contents
import re # Use to parse file names for a match

# Constants
debug = False

def open_file(ci_file):
    '''
    Open the CI file
    '''
    ci_lines = [] # Blank list to add CI's

    # Check to see if cmd_file exists
    if exists(ci_file):
        file_exists = True
    else:
        file_exists = False
        sys.exit("\nSorry, the input file: %s does not exist in the local folder.\n" % ci_file)

    # Open the file and read the contents into the list
    with open(ci_file) as f:
        ci_lines = f.read().splitlines()

    # Get change number from file name.
    change_num = ci_file.split(".")[0]

    # Close the file
    #f.close()

    return (ci_lines, change_num)

def create_dict(ci_item, username, password):
    '''
    Create dictionary for Netmiko connection
    '''
    my_dict = {
        'device_type': 'cisco_ios',
        'host': ci_item,
        'username': username,
        'password': password
    }
    return my_dict

def write_log(router_data, ci_item, change_num):
    '''
    #Write out the log file based on Change number, CI and datetime
    '''
    # Get a list of the files in the current directory
    dir_files = os.listdir('.')

    # Build the search string.  Ignore any special characters in the change_num
    # Concatenate the change_num with RE.  Read until '.', must end with '.log'
    my_string = change_num + '_' + ci_item + r'([^.]*(.log))'

    # initialize mode to '_PRE'
    mode = '_PRE'

    # If a filename starting with the change_num already exists,
    # append POST to the fie name.
    for i in dir_files:
        re_pattern = re.search(my_string, i, re.IGNORECASE)
        if re_pattern:
            mode = '_POST'
            break

    # Create log file name
    now = datetime.now()
    stamp = now.strftime("_%Y_%m_%d_%H_%M_%S")
    log_file_name = change_num + '_' + ci_item + stamp + mode + ".log"

    # Write log
    log_file = open(log_file_name, 'w')
    log_file.write(router_data)
    return log_file_name

def get_data(ci_item, cmd_file, change_num, username, password):
    '''
    Open a connection to each CI and run commands from cmd file.
    Write output to log file for each CI.
    '''
    my_dict = create_dict(ci_item, username, password)
    net_connect = ConnectHandler(**my_dict)
    router_data = net_connect.send_config_from_file(config_file=cmd_file)
    log_file_name = write_log(router_data, ci_item, change_num)
    print "Done: %s" % log_file_name
    print

def main():
    '''
    Open the text file and iterate through the CI's.
    Open a connection to each CI and run commands from cmd file.
    Write output to log file for each CI.
    Spawn a thread for each connection
    '''
    # prompt for input of ci_file and cmd_file
    ci_file = raw_input("\nEnter the CHG filename: ")
    # Open file.  Get list of CI's and change number
    ci_lines, change_num = open_file(ci_file)
    print "Accepted"
    cmd_file = raw_input("\nEnter the command filename: ")
    print "Accepted. Enter password:"
    print

    # Get user name from system context, prompt for password.
    username = getuser()
    password = getpass()
    print "Accepted.  Processing CI's..."
    print

    # Start the clock
    start_time = datetime.now()

    # Iterate through list.  Create a thread for each CI.
    for ci_item in ci_lines:
        my_thread = threading.Thread(target=get_data, args=(ci_item,cmd_file,change_num,username,password))
        my_thread.start()

    # Wait until all threads complete
    main_thread = threading.currentThread()
    for thread_name in threading.enumerate():
        if thread_name != main_thread:
            if debug:
                print thread_name
            thread_name.join()

    # Print elapsed run time
    print "\nElapsed time: " + str(datetime.now() - start_time)
    print

if __name__ == '__main__':
    main()
