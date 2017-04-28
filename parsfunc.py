"""
Parse Dictionary Function Library
Author: Robert Becker
Date: April 17, 2017
Purpose: Recursive functions used to parse a JSON dictionary

Output will look like this...
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


def dictlevel(indict, dlevel, fileio, lname):
    """
    Input parameters:
    indict = dictionary to be parsed
    dlevel = current dictionary level
    fileio = class for file operations
    lname  = last name of desired player stats

    Function loops through dictionary keys and examines values
    If function finds a nested dictionary, it calls itself
    If function finds a list, it calls listlevel to parse the list
    If function finds a normal value, it prints the value
    If value is for desired player, print name and all stats for player
    """

    # get the list of dictionary keys at the current level
    keylist = list(indict.keys())

    # if desired player is in this part of dictionary, start printing
    if 'name' in keylist and str(indict['name']) == lname:
        playermatch = True
        print('Player stats for: ' + lname)
    else:
        playermatch = False

    # loop thru each dictionary key at the current level
    for dictkey in keylist:

        # create output string showing level and current dictionary key
        outputstr = 'Level ' + str(dlevel) + ' Key=' + dictkey + ' '

        # test if current value is a nested dictionary
        if isinstance(indict[dictkey], dict):
            # write output to indicate beginning of nested dictionary
            dictvalue = outputstr + 'SubDictionary--Begin'
            fileio.writefile(dictvalue+"\n")

            # recursive call to parse nested dictionary, increase level
            dictlevel(indict[dictkey], dlevel+1, fileio, lname)

            # write output to indicate end of nested dictionary
            dictvalue = outputstr + 'SubDictionary--End'
            fileio.writefile(dictvalue+"\n")

        # test if current value is a list
        elif isinstance(indict[dictkey], list):
            # write output to indicate beginning of list
            dictvalue = outputstr + 'List--Begin'
            fileio.writefile(dictvalue+"\n")

            # call function to parse list, level stays same
            listlevel(indict[dictkey], dlevel, fileio, dictkey, lname)

            # write output to indicate end of list
            dictvalue = outputstr + 'List--End'
            fileio.writefile(dictvalue+"\n")

        # no dictionary, no list, must have a value
        else:
            # write output to show value from dictionary key
            dictvalue = outputstr + 'Value=' + str(indict[dictkey])
            fileio.writefile(dictvalue+"\n")

            # print game stat value if this is our guy
            if playermatch:
                print(dictkey + ' = ' + str(indict[dictkey]))


def listlevel(inlist, llevel, fileio, dkey, lname):
    """
    Input parameters:
    inlist = list to be parsed
    llevel = current dictionary level, will not change
    fileio = class for file operations
    dkey   = current dictionary key, needed for output
    lname  = last name of desired player stats

    Function loops through a list and examines list entries
    If function finds a nested dictionary, it calls dictlevel
    If function finds a list, it calls itself to parse the list
    If function finds a normal value, it prints the value
    """

    # loop thru each list entry at the current level
    for listentry in inlist:

        # create output string showing level and current dictionary key
        outputstr = 'Level ' + str(llevel) + ' Key=' + dkey + ' '

        # test if current list entry is a nested dictionary
        if isinstance(listentry, dict):
            # write output to indicate beginning of nested dictionary
            dictvalue = outputstr + 'SubDictionary--Begin'
            fileio.writefile(dictvalue+"\n")

            # call dictlevel to parse nested dictionary, increase level
            dictlevel(listentry, llevel+1, fileio, lname)

            # write output to indicate end of nested dictionary
            dictvalue = outputstr + 'SubDictionary--End'
            fileio.writefile(dictvalue+"\n")

        # test if current entry is a list
        elif isinstance(listentry, list):
            # write output to indicate beginning of nested list
            dictvalue = outputstr + 'List--Begin'
            fileio.writefile(dictvalue+"\n")

            # recursive call to parse nested list, level stays the same
            listlevel(listentry, llevel, fileio, dkey, lname)

            # write output to indicate end of nested list
            dictvalue = outputstr + 'List--End'
            fileio.writefile(dictvalue+"\n")

        # no dictionary, no list, must have a value
        else:
            # write output to show value from list entry
            dictvalue = outputstr + 'Value=' + str(listentry)
            fileio.writefile(dictvalue+"\n")
