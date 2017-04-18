"""
Json Dictionary Parsing Program
Author: Robert Becker
Date: April 17, 2017
Purpose: Traverse a json dictionary printing levels and values
Uses: json and requests libraries, response, and a recursive function

Read a config file to get the url of a json dictionary and store url
Load url into dictionary variable and call recursive function to parse
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

# loop thru file and store parameters
while configrec != "":
    if configrec[:4] == 'url=':
        url = configrec[4:]
    configrec = configfile.readline()

# close config file
configfile.close()

# get response from url and convert text into dictionary
urlresponse = requests.get(url)
dictdata = json.loads(urlresponse.text)

filehandler = FileOps()
filehandler.openfile()

# call recursive function to parse json, pass dictionary and top level 1
parsfunc.dictlevel(dictdata, 1, filehandler)
