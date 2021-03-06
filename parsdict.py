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
import sys
import json
import requests
import parsfunc


# set logging, config, and output file locations
CONFIG_INI = 'parsdict_config.ini'
LOGGING_INI = 'parsdict_logging.ini'
PARSED_OUT = '../DataFiles/dictparsed.txt'

# setup logging and log initial message
logging.config.fileConfig(LOGGING_INI)
logger = logging.getLogger(__name__)
logger.info('Executing script: parsdict.py')


class ConfigLoadError(ValueError):
    pass


class JsonLocationKeyError(ValueError):
    pass


class JsonKeyMissingError(ValueError):
    pass


class LoadDictionaryError(ValueError):
    pass


class FileOps:
    """
    File handling routing for dictionary output file

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


def get_command_arguments():
    """
    last_name  required, name of player used to select data
    input      required, specifies data source, naming pattern url__ or file__
    output     optional, if provided a file of dictionary elements is created
                   -o, --output, this is all that needs to be specified if used
    config     optional, if provided will serve as the config.ini location
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
    parser.add_argument(
        '-c,'
        '--config',
        help='Config file location',
        dest='config',
        type=str
    )

    argue = parser.parse_args()

    # log command line arguments and if optional output file was chosen
    logger.info('parsdict arguments: ' + argue.last_name + ' ' + argue.input)
    if argue.output:
        logger.info('Writing dictionary entries to file ' + PARSED_OUT)

    return argue


def get_config_file(config_default, opt_config=None):

    config = configparser.ConfigParser()

    # override config location if optional command line argument specified
    if opt_config:
        configini = opt_config
    else:
        configini = config_default

    logger.info('Config file location = ' + configini)

    # open config file to verify existence, then read and return
    try:
        config.read_file(open(configini))
        config.read(configini)
        return config
    except Exception as e:
        errmsg = 'Error loading Configuration file. . .'
        logger.critical(errmsg)
        logger.exception(e)
        raise ConfigLoadError(errmsg)


def get_json_location(jsonkey, config):

    # don't have proper Config paramater based on Command Line argument
    if jsonkey[:4] != 'file' and jsonkey[:3] != 'url':
        errmsg = 'Config DataSource key must start with url or file'
        logger.critical(errmsg)
        raise JsonLocationKeyError(errmsg)

    # verify input key is in DataSource before setting source location
    if config.has_option("DataSources", jsonkey):
        return config.get("DataSources", jsonkey)
    else:
        errmsg = jsonkey + ' key missing from config DataSource'
        logger.critical(errmsg)
        raise JsonKeyMissingError(errmsg)


def load_dictionary(jsonkey, jsonplace):

    # log dictionary location
    logger.info('Loading dictionary from location: ' + jsonplace)

    # get JSON data from file if desired and load into dictionary
    if jsonkey[:4] == 'file':
        try:
            jfile = open(jsonplace, 'r')
            jdata = jfile.readline()
            jfile.close()
            dictdata = json.loads(jdata)
            return dictdata
        except Exception as e:
            errmsg = 'Error loading dictionary from file. . .'
            logger.critical(errmsg)
            logger.exception(e)
            raise LoadDictionaryError(errmsg)
    # get JSON data from url if desired and load into dictionary
    elif jsonkey[:3] == 'url':
        try:
            jsonresp = requests.get(jsonplace)
            dictdata = json.loads(jsonresp.text)
            return dictdata
        except Exception as e:
            errmsg = 'Error loading dictionary from url. . .'
            logger.critical(errmsg)
            logger.exception(e)
            raise LoadDictionaryError(errmsg)


def print_player_info(playerdict, lastname):

    # get list of dictionary keys from returned player data
    keylist = list(playerdict.keys())

    # print heading for player followed by his boxscore data
    print("Player: " + lastname)
    for dictkey in keylist:
        print(dictkey + " = " + str(playerdict[dictkey]))


def main():

    args = get_command_arguments()

    # load config file into memory
    try:
        configdata = get_config_file(CONFIG_INI, args.config)
    except ConfigLoadError:
        return 1

    # get json dictionary information from config file
    try:
        jsonloc = get_json_location(args.input, configdata)
    except JsonLocationKeyError:
        return 10
    except JsonKeyMissingError:
        return 11

    # load json dictionary into memory
    try:
        jsondict = load_dictionary(args.input, jsonloc)
    except LoadDictionaryError:
        return 20

    # open output file if command line argument --output is true
    output_file = FileOps(args.output)
    output_file.openfile(PARSED_OUT)

    # call function to extract player data from dictionary and print it
    logger.info('Searching dictionary for ' + args.last_name)

    myplayer = parsfunc.search_dictionary(jsondict,
                                          1,
                                          args.last_name,
                                          output_file)

    print_player_info(myplayer, args.last_name)

    # close output file (if it was opened)
    output_file.closefile()

    return 0


if __name__ == '__main__':
    cc = main()
    logger.info('parsdict.py completion code: ' + str(cc))
    sys.exit(cc)
