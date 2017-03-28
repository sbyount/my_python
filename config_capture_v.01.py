#!/usr/bin/env python
'''
Script to record pre-change and post-change captures using Netmiko.
Reads CI's in from a text file: "CHG000xxxx.txt" in the local directory
Prompts the user for the text file name.  Change number is used for output capture files.

Script runs standard commands and saves a copy of the running config on router
according to the standard.
Script creates output log file int the following format:
    "CHG000xxxx_CINAME_DATETIME.log"
'''

# Imports
from netmiko import ConnectHandler
from getpass import getuser, getpass
import time
import datetime
import sys
from os.path import exists

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

    if debug:
        # test print the command data (remove)
        print "\nTest print the CI list."
        print ci_lines
        print "\nPrint change number."
        print change_num
        print

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
    # Write logs
    now = datetime.datetime.now()
    stamp = now.strftime("_%Y_%m_%d_%H_%M_%S")

    log_file_name = change_num + '_' + ci_item + stamp + ".log"
    log_file = open(log_file_name, 'w')
    log_file.write(router_data)
    return log_file_name

def main():
    '''
    Open the text file and iterate through the CI's.
    Open a connection to each CI and run commands from cmd file.
    Write output to log file for each CI.
    '''
    # prompt for input of ci_file and cmd_file
    ci_file = raw_input("\nEnter the CI filename: ")
    ci_lines, change_num = open_file(ci_file)
    print
    cmd_file = raw_input("\nEnter the command filename: ")
    print

    # Get user name from system context, prompt for password.
    username = getuser()
    password = getpass()
    print

    for ci_item in ci_lines:
        my_dict = create_dict(ci_item, username, password)
        net_connect = ConnectHandler(**my_dict)
        #router_data = net_connect.send_command("show ver")
        #router_data = net_connect.send_config_from_file(config_file='cmd.txt')
        router_data = net_connect.send_config_from_file(config_file=cmd_file)
        log_file_name = write_log(router_data, ci_item, change_num)
        print "Done: %s" % log_file_name
        print

    if debug:
        # Write test log file
        print "\nCreating test log file."
        router_data = "Test router data."

        # Just use the first item
        ci_item = ci_lines[0]
        print ci_item

if __name__ == '__main__':
    main()
