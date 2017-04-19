"""
JSON Dictionary Parsing Program
Author: Robert Becker
Date: April 17, 2017
Purpose: Traverse a JSON dictionary printing all levels and values
Uses: JSON and requests libraries, response, and 2 recursive functions

Read config file to get location of a json dictionary (url or local file)
Load dictionary from location (local file has preference over url)
Call dictlevel function to begin parsing process

Config file should have 1 line per location. Example:
url=http://somewebsite.com/somedirectory/somefile.json
file=../DataFiles/somefile.json
"""


import json
import requests
import parsfunc


class FileOps:
    """
    docstring for FileOps
    """
    def openfile(parsed):
        parsed.outfile = open('../DataFiles/dictparsed.txt', 'w')

    def writefile(parsed, stringout):
        parsed.outfile.write(stringout)

    def closefile(parsed):
        parsed.outfile.close()


# open config file and read first line
configfile = open('../DataFiles/config_parsdict.py', 'r')
configrec = configfile.readline()

# initialize variables for possible locations
jsonurl = ""
jsonfile = ""

# loop thru config file and store parameters
while configrec != "":
    if configrec[:4] == 'url=':
        jsonurl = configrec[4:].rstrip('\n')
    elif configrec[:5] == 'file=':
        jsonfile = configrec[5:].rstrip('\n')
    configrec = configfile.readline()

# close config file
configfile.close()

# get JSON data from file if provided and load into dictionary
if jsonfile != "":
    print('Dictionary location = ' + jsonfile)
    jfile = open(jsonfile, 'r')
    jdata = jfile.readline()
    dictdata = json.loads(jdata)
    jfile.close()
# get response from url if provided and convert text into dictionary
elif jsonurl != "":
    print('Dictionary location = ' + jsonurl)
    jsonurlresp = requests.get(jsonurl)
    dictdata = json.loads(jsonurlresp.text)

filehandler = FileOps()
filehandler.openfile()

# call recursive function to parse JSON, pass dictionary and level 1
parsfunc.dictlevel(dictdata, 1, filehandler)

# close output file
filehandler.closefile()
