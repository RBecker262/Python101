"""
JSON Dictionary Parsing Program
Author: Robert Becker
Date: April 17, 2017
Purpose: Parse a JSON dictionary and return player info or print all data
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
import configparser
import logging
import logging.config
import json
import requests
import parsfunc


class file_ops:
    """
    Define open, write, and close methods for class file_ops
    Command line arg passed to determine if output should be produced
    """
    def openfile(self, parsed_output, writeoutput):
        if writeoutput:
            self.outfile = open(parsed_output, 'w')

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
        '--output',
        help='Indicates output file created (y or n)',
        dest='output',
        default='N',
        type=str,
    )
    return parser.parse_args()


def main():
    # set logging, config, and output file locations
    logging_ini = '../DataFiles/logging.ini'
    config_ini = '../DataFiles/config_parsdict.ini'
    parsed_out = '../DataFiles/dictparsed.txt'

    # setup logging
    logging.config.fileConfig(logging_ini)
    logger = logging.getLogger(__name__)
    logger.info('Executing parsdict module')

    # get command line arguments and set boolean to write output file or not
    args = parse_arguments()
    if args.output.upper() == "Y":
        writeme = True
    else:
        writeme = False

    # log command line arguments
    logger.info('parsdict arguments: ' + args.last_name + ' ' + args.input)

    # get location from config file using command line argument as the key
    config = configparser.ConfigParser()
    config.read(config_ini)
    jsonloc = config.get("DataSources", args.input)

    # print dictionary location that was chosen
    print('Dictionary location = ' + jsonloc)

    # get JSON data from file if desired and load into dictionary
    if args.input[:4] == 'file' and jsonloc != "":
        jfile = open(jsonloc, 'r')
        jdata = jfile.readline()
        dictdata = json.loads(jdata)
        jfile.close()
    # get JSON data from url if desired and load into dictionary
    elif args.input[:3] == 'url' and jsonloc != "":
        jsonresp = requests.get(jsonloc)
        dictdata = json.loads(jsonresp.text)
    # don't have proper Config paramater based on Command Line argument
    else:
        quit('Command line input inconsistent with Config file: ' + args.input)

    # open output file parsedout if command line argument --output is true
    output_file = file_ops()
    output_file.openfile(parsed_out, writeme)

    # call recursive function to parse JSON dictionary
    myplayer = parsfunc.dictlevel(dictdata,
                                  1,
                                  args.last_name,
                                  output_file,
                                  writeme)

    # get list of keys from returned player data and print header
    myplayerkeys = list(myplayer.keys())

    # print heading for player followed by his boxscore data
    print("Player: " + args.last_name)
    for dictkey in myplayerkeys:
        print(dictkey + " = " + myplayer[dictkey])

    # close output file (if it was opened)
    output_file.closefile(writeme)


if __name__ == '__main__':
    main()
