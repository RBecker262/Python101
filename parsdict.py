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

Config file can have many locations defined. Order of entries is irrelevant.
Example:
url=http://somewebsite.com/somedirectory/somefile.json
url1=http://somewebsite.com/somedirectory/someothefile.json
file1=../DataFiles/somelocalfile.json
file2=../DataFiles/anotherlocalfile.json
"""


import argparse
import json
import requests
import parsfunc


class file_ops:
    """
    Define open, write, and close methods for class file_ops
    Command line arg passed to determine if output should be produced
    """
    def openfile(self, writeoutput):
        if writeoutput:
            self.outfile = open('../DataFiles/dictparsed.txt', 'w')

    def writefile(self, stringout, writeoutput):
        if writeoutput:
            self.outfile.write(stringout)

    def closefile(self, writeoutput):
        if writeoutput:
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
        help='Input data source; specify url(n) or file(n)',
        dest='input',
        type=str,
    )
    parser.add_argument(
        '-o',
        '--output',
        help='Indicates output file created (y or n)',
        dest='output',
        type=str,
    )
    return parser.parse_args()


def main():
    # get command line arguments
    args = parse_arguments()

    # set boolean variable if we should write output file or not
    if args.output.upper() == "Y":
        writeme = True
    else:
        writeme = False

    # initialize variable for possible dictionary locations
    jsonloc = ""
    argloc = args.input + "="
    loclen = len(argloc)

    # open config file and read first line
    configfile = open('../DataFiles/config_parsdict.py', 'r')
    configrec = configfile.readline()

    # loop thru config file and store desired location
    while configrec != "":
        if configrec[:loclen] == argloc:
            jsonloc = configrec[loclen:].rstrip('\n')
        configrec = configfile.readline()

    # close config file
    configfile.close()

    # get JSON data from file if desired and load into dictionary
    if args.input[:4] == 'file' and jsonloc != "":
        print('Dictionary location = ' + jsonloc)
        jfile = open(jsonloc, 'r')
        jdata = jfile.readline()
        dictdata = json.loads(jdata)
        jfile.close()
    # get JSON data from url if desired and load into dictionary
    elif args.input[:3] == 'url' and jsonloc != "":
        print('Dictionary location = ' + jsonloc)
        jsonresp = requests.get(jsonloc)
        dictdata = json.loads(jsonresp.text)
    # don't have proper Config paramater based on Command Line argument
    else:
        quit('Command line input inconsistent with Config file: ' + args.input)

    # use class to open file which is passed to dictionary function
    output_file = file_ops()
    output_file.openfile(writeme)

    # call recursive function to parse JSON dictionary
    parsfunc.dictlevel(dictdata, 1, args.last_name, output_file, writeme)

    # close output file
    output_file.closefile(writeme)


if __name__ == '__main__':
    main()
