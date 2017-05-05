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


# set logging, config, and output file locations
CONFIG_INI = '../DataFiles/parsdict_config.ini'
LOGGING_INI = '../DataFiles/parsdict_logging.ini'
PARSED_OUT = '../DataFiles/dictparsed.txt'

# setup logging and log initial message
logging.config.fileConfig(LOGGING_INI)
logger = logging.getLogger(__name__)
logger.info('Executing script: parsdict.py')


class FileOps:
    """
    __init__   sets writeoutput to True/False based on -o command line argument
    openfile   passed the file location, opens if writeoutput is True
    writefile  passed the output string, writes record if writeoutput is True
    closefile  closes file if writeoutput is True
    """

    def __init__(self, writeme):
        self.writeoutput = writeme

    def openfile(self, parsed_output):
        if self.writeoutput:
            self.outfile = open(parsed_output, 'w')

    def writefile(self, stringout):
        if self.writeoutput:
            self.outfile.write(stringout)

    def closefile(self):
        if self.writeoutput:
            self.outfile.close()


def parse_arguments():
    """
    last_name  required, name of player used to select data
    input      required, specifies data source, naming pattern url__ or file__
    output     optional, if provided a file of dictionary elements is created
                   -o, --output, this is all that needs to be specified if used
    """

    parser = argparse.ArgumentParser('Search Game Data for Player Statistics')
    parser.add_argument(
        help='Player last name',
        dest='last_name',
        type=str
    )
    parser.add_argument(
        '-i',
        '--input',
        help='Input data source; specify url(n) or file(n)',
        dest='input',
        type=str
    )
    parser.add_argument(
        '-o',
        '--output',
        help='Output file is created if specified',
        dest='output',
        action='store_true'
    )
    return parser.parse_args()


def main():
    # get command line arguments
    args = parse_arguments()

    # log command line arguments and if optional output file was chosen
    logger.info('parsdict arguments: ' + args.last_name + ' ' + args.input)
    if args.output:
        logger.info('Writing dictionary entries to file ' + PARSED_OUT)

    # get location from config file using command line argument as the key
    config = configparser.ConfigParser()
    config.read(CONFIG_INI)

    # verify input key is in DataSource before setting source location
    if config.has_option("DataSources", args.input):
        jsonloc = config.get("DataSources", args.input)
    else:
        logger.critical(args.input + ' key missing from config DataSource')
        return

    # log dictionary location
    logger.info('Loading dictionary from location: ' + jsonloc)

    # get JSON data from file if desired and load into dictionary
    if args.input[:4] == 'file':
        try:
            jfile = open(jsonloc, 'r')
            jdata = jfile.readline()
            dictdata = json.loads(jdata)
            jfile.close()
        except Exception as e:
            logger.critical('Error loading dictionary from file. . .')
            logger.exception(e)
            return
    # get JSON data from url if desired and load into dictionary
    elif args.input[:3] == 'url':
        try:
            jsonresp = requests.get(jsonloc)
            dictdata = json.loads(jsonresp.text)
        except Exception as e:
            # ex_type, ex, tb = sys.exec_info()
            logger.critical('Error loading dictionary from url. . .')
            logger.exception(e)
            return
    # don't have proper Config paramater based on Command Line argument
    else:
        logger.critical('Config DataSource key must start with url or file')
        return

    # open output file parsedout if command line argument --output is true
    output_file = FileOps(args.output)
    output_file.openfile(PARSED_OUT)

    # log call to function to parse the json dictionary
    logger.info('Searching the dictionary for ' + args.last_name)

    # call recursive function to parse JSON dictionary
    myplayer = parsfunc.dictlevel(dictdata,
                                  1,
                                  args.last_name,
                                  output_file)

    # get list of keys from returned player data and print header
    myplayerkeys = list(myplayer.keys())

    # print heading for player followed by his boxscore data
    print("Player: " + args.last_name)
    for dictkey in myplayerkeys:
        print(dictkey + " = " + str(myplayer[dictkey]))

    # close output file (if it was opened)
    output_file.closefile()


if __name__ == '__main__':
    main()
