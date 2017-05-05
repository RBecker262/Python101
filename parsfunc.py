"""
Parse Dictionary Function Library
Author: Robert Becker
Date: April 17, 2017
Purpose: Recursive functions used to find player data in json dictionary

If output file desired, report will look like this...
Level n   Key=abc Value=123

Level n   Key=def SubDictionary--Begin
Level n+1 Key=def Value=456
Level n+1 Key=def Value=789
Level n   Key=def SubDictionary--End

Level n   Key=xyz List--Begin
Level n   Key=xyz Value=987
Level n   Key=xyz Value=321
Level n   Key=xyz List--End

A list can contain dictionaries so you might see this...
Level n   Key=444 List--Begin
Level n   Key=444 Value=listentry1
Level n   Key=444 SubDictionary--Begin
Level n+1 Key=555 Value=dictentry1
Level n+1 Key=555 Value=dictentry2
Level n   Key=444 SubDictionary--End
Level n   Key=444 Value=listentry3 (because SubDictionary was entry 2)
Level n   Key=444 List--End
"""


import logging


def search_dictionary(indict, dlevel, lname, fileio):
    """
    Input parameters:
    indict  = dictionary to be parsed
    dlevel  = current dictionary level
    lname   = last name of desired player stats
    fileio  = class for file operations

    Function loops through dictionary keys and examines values
    If function finds a nested dictionary, call itself to parse next level
    If function finds a list, call listlevel to parse the list
    If function finds a normal value, it writes output file if desired
    As soon as player data is found return to previous recursion level
    """

    logger = logging.getLogger(__name__)
    logger.debug('Dictionary level: ' + str(dlevel))

    # get dictionary key list from current level and return if it's our player
    keylist = list(indict.keys())

    if 'name' in keylist and str(indict['name']) == lname:
        logger.info(str(len(keylist)) + ' stats found for ' + lname)
        return indict

    # loop thru each dictionary key at the current level
    for dictkey in keylist:

        outputstr = 'Level ' + str(dlevel) + ' Key=' + dictkey + ' '

        # test if current value is a nested dictionary
        if isinstance(indict[dictkey], dict):
            # write output to indicate beginning of nested dictionary
            dictvalue = outputstr + 'SubDictionary--Begin'
            fileio.writefile(dictvalue+"\n")

            # recursive call to parse nested dictionary, increase level #
            logger.debug('Recursive call to search for key: ' + dictkey)

            myplayerdata = search_dictionary(indict[dictkey],
                                             dlevel+1,
                                             lname,
                                             fileio)

            logger.debug('Returned from recursive call for key: ' + dictkey)

            # if player data found, return data to previous recursion level
            if myplayerdata:
                return myplayerdata

            # write output to indicate end of nested dictionary
            dictvalue = outputstr + 'SubDictionary--End'
            fileio.writefile(dictvalue+"\n")

        # test if current value is a list
        elif isinstance(indict[dictkey], list):
            # write output to indicate beginning of list
            dictvalue = outputstr + 'List--Begin'
            fileio.writefile(dictvalue+"\n")

            # call function to search list, level stays same
            logger.debug('Call search_list for dictionary key: ' + dictkey)

            myplayerdata = search_list(indict[dictkey],
                                       dlevel,
                                       dictkey,
                                       lname,
                                       fileio)

            logger.debug('Returned from parsing list for key: ' + dictkey)

            # If player data found, return data to previous recursion level
            if myplayerdata:
                return myplayerdata

            # write output to indicate end of list
            dictvalue = outputstr + 'List--End'
            fileio.writefile(dictvalue+"\n")

        # no dictionary, no list, must have a value
        else:
            # write output to show value from dictionary key
            dictvalue = outputstr + 'Value=' + str(indict[dictkey])
            fileio.writefile(dictvalue+"\n")

    # return empty dictionary if nothing found within this level
    return {}


def search_list(inlist, llevel, dkey, lname, fileio):
    """
    Input parameters:
    inlist  = list to be parsed
    llevel  = current dictionary level, will not change
    dkey    = current dictionary key, needed for output
    lname   = last name of desired player stats
    fileio  = class for file operations

    Function loops through a list and examines list entries
    If function finds a nested dictionary, it calls dictlevel
    If function finds a list, it calls itself to parse the list
    As soon as player data is found return to previous recursion level
    """

    logger = logging.getLogger(__name__)
    logger.debug('List within dictionary key: ' + dkey)

    # loop thru each list entry at the current level
    for listentry in inlist:

        outputstr = 'Level ' + str(llevel) + ' Key=' + dkey + ' '

        # test if current list entry is a nested dictionary
        if isinstance(listentry, dict):
            # write output to indicate beginning of nested dictionary
            dictvalue = outputstr + 'SubDictionary--Begin'
            fileio.writefile(dictvalue+"\n")

            # recursive call to parse nested dictionary, increase level #
            logger.debug('Recursive call search_dictionary from search_list')

            myplayerdata = search_dictionary(listentry,
                                             llevel+1,
                                             lname,
                                             fileio)

            logger.debug('Returned from recursive call for key: ' + dkey)

            # if player data found, return data to previous recursion level
            if myplayerdata:
                return myplayerdata

            # write output to indicate end of nested dictionary
            dictvalue = outputstr + 'SubDictionary--End'
            fileio.writefile(dictvalue+"\n")

        # test if current entry is a list
        elif isinstance(listentry, list):
            # write output to indicate beginning of nested list
            dictvalue = outputstr + 'List--Begin'
            fileio.writefile(dictvalue+"\n")

            # recursive call to search nested list, level stays the same
            logger.debug('Recursive call to listlevel function')

            myplayerdata = search_list(listentry,
                                       llevel,
                                       dkey,
                                       lname,
                                       fileio)

            logger.debug('Returned from recursive call to search_list')

            # if player data found, return data to previous recursion level
            if myplayerdata:
                return myplayerdata

            # write output to indicate end of nested list
            dictvalue = outputstr + 'List--End'
            fileio.writefile(dictvalue+"\n")

        # no dictionary, no list, must have a value
        else:
            # write output to show value from list entry
            dictvalue = outputstr + 'Value=' + str(listentry)
            fileio.writefile(dictvalue+"\n")

    # return empty dictionary if nothing found within this level
    return {}
