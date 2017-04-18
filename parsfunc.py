"""
Parse Dictionary Function Library
Author: Robert Becker
Date: April 17, 2017
Purpose: Recursive function to parse dictionary
"""


def dictlevel(indict, inlevel, fileio):
    """
    Input parameters:
    indict = dictionary to be parsed
    inlevel = current dictionary level

    As the module finds a sub dictionary when at the current level
    It recursively calls itself passing sub dictionary and new level
    It will continue to do this until all levels have been parsed
    """

    # get the list of dictionary keys at the current level
    keylist = list(indict.keys())

    # loop thru each key at the current level
    for dictkey in keylist:

        # create output string showing level and current dictionary key
        outputstr = 'Level ' + str(inlevel) + ' ' + dictkey + ' '

        # test if current key is a dictionary or other value
        if isinstance(indict[dictkey], dict):
            # print output and make recursive call for next dictionary level
            dictvalue = outputstr + 'Subdictionary'
            print(dictvalue)
            fileio.writefile(dictvalue+"\n")
            dictlevel(indict[dictkey], inlevel+1, fileio)
        else:
            # print output showing first 20 bytes of dictionary value
            dictvalue = outputstr + str(indict[dictkey])[:20]
            print(dictvalue)
            fileio.writefile(dictvalue+"\n")
