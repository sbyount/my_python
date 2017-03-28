#!\usr\bin\env python
'''
Script to record pre-change and post-change captures using Netmiko and Paramiko.

Reads CI's in from a text file: "CHG000xxxx.txt" in the local directory
Prompts the user for the text file name.  Change number is used for output capture files.
Model and DIR commands are predefined.

Script runs standard commands and saves a copy of the running config on router
according to the standard.

Script creates output text file int the following format:
    "CHG000xxxx_CINAME_DATETIME.txt"
'''

import netmiko
import time
import sys
from os.path import exists

def open_file(ci_file):
    '''
    Open the CI file
    '''
    ci_list = [] # Blank list to contain CI's

    # Check to see if cmd_file exists
    if exists(ci_file):
        file_exists = True
    else:
        file_exists = False
        sys.exit("\nSorry, the input file: %s does not exist.\n" % ci_file)

    # Open the file and read the contents into the list
    ci_file_pointer = open(ci_file)
    ci_list = ci_file_pointer.read()

    # strip name
    change_num = ci_file.split(".")[0]

    # Close the file
    #ci_file_pointer.close()

    # test print the command data (remove)
    print ci_list
    print change_num
    return ci_list

def write_log(router_data):
    '''
    #Write out the log file based on Change number, CI and datetime

    # Write logs
    now = datetime.datetime.now()
    stamp = now.strftime("_%Y_%m_%d_%H_%M_%S")

    log_file_name = change_num + stamp + ".log"
    log_file = open(log_file_name, 'w')
    log_file.write(router_data)
    '''
def main():
    '''
    Open the text file and iterate through the CI's.
    Open a connection to each CI and run commands.
    Check model and specify DIR command.
    Write output to file using YAML or JSON
    '''
    # prompt for input of ci_file
    ci_file = raw_input("Enter the CI filename: ")
    open_file(ci_file)

    # show flash:

if __name__ == '__main__':
    main()
