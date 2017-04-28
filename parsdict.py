"""
JSON Dictionary Parsing Program
Author: Robert Becker
Date: April 17, 2017
Purpose: Traverse a JSON dictionary printing all levels and values
Uses: JSON and requests libraries, response, and 2 recursive functions

Get Command Line arguments to determine data source and player stats desired
Read config file to get possible locations of a json dictionary (url or file)
Load dictionary from location (determined by Command Line arguments)
Call dictlevel function to begin parsing process

Config file should have 1 line per location. Example:
url=http://somewebsite.com/somedirectory/somefile.json
file=../DataFiles/somefile.json
"""


import argparse
import json
import requests
import parsfunc


class file_ops:
    """
    Define open, write, and close methods for class file_ops
    """
    def openfile(self):
        self.outfile = open('../DataFiles/dictparsed.txt', 'w')

    def writefile(self, stringout):
        self.outfile.write(stringout)

    def closefile(self):
        self.outfile.close()


def parse_arguments():
    # instantiate an "ArgumentParser" from the argparse module in stdlib
    # the first argument of the contstructor is the "help"
    # https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    parser = argparse.ArgumentParser('Search Game Data for Batter Statistics')
    parser.add_argument(
        help='Player last name',
        type=str,
        dest='last_name',
    )
    parser.add_argument(
        '-i',
        '--input',
        help='Input data source; specify url or file',
        dest='input',
        type=str,
    )
    return parser.parse_args()


# get command line arguments
args = parse_arguments()

# initialize variables for possible dictionary locations
jsonurl = ""
jsonfile = ""

# open config file and read first line
configfile = open('../DataFiles/config_parsdict.py', 'r')
configrec = configfile.readline()

# loop thru config file and store parameters
while configrec != "":
    if configrec[:4] == 'url=':
        jsonurl = configrec[4:].rstrip('\n')
    elif configrec[:5] == 'file=':
        jsonfile = configrec[5:].rstrip('\n')
    configrec = configfile.readline()

# close config file
configfile.close()

# get JSON data from file if desired and load into dictionary
if args.input == 'file' and jsonfile != "":
    print('Dictionary location = ' + jsonfile)
    jfile = open(jsonfile, 'r')
    jdata = jfile.readline()
    dictdata = json.loads(jdata)
    jfile.close()
# get JSON data from url if desired and load into dictionary
elif args.input == 'url' and jsonurl != "":
    print('Dictionary location = ' + jsonurl)
    jsonurlresp = requests.get(jsonurl)
    dictdata = json.loads(jsonurlresp.text)
# don't have proper Config paramater based on Command Line argument
else:
    quit('Command line input inconsistent with Config file: ' + args.input)

# use class to open file which is passed to dictionary function
filehandler = file_ops()
filehandler.openfile()

# call recursive function to parse JSON dictionary
parsfunc.dictlevel(dictdata, 1, filehandler, args.last_name)

# close output file
filehandler.closefile()
