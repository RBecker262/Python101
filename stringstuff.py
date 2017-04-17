"""
My first Python Function Library
Author: Robert Becker
Date: April 11, 2017
Purpose: Functions to count and manipulate strings
"""


def strlen(countstr):
    """
    Function takes a passed string and determines the length
    The length of the string is returned
    """

    # string index starts at 0, loop until IndexError (end of string)
    i = 0

    # loop until an IndexError condition is reached
    while True:

        # try addressing the next slice, add 1 to i if successful
        try:
            if countstr[i] != "":
                i = i + 1
        # at end of list return i as the length of the string
        except IndexError as whyme:
            return (i)


def backwards(reverseme, skipchar):
    """
    Function is passed a string and a number used to skip characters
    Two string results are created and returned in a tuple
    First string will contain the original string in reverse order
    Second string will contain every nth character in reverse order
    """

    # initialize result strings and length of intput string
    backstr = ""
    backstrskip = ""
    l = strlen(reverseme)

    # set default of 1 if skip character parameter is < 0 or > length
    if skipchar < 0 or skipchar > l:
        skipchar = 1
    # guarantee that we have a whole number
    else:
        skipchar = int(skipchar)

    # slice thru string and create reverse string and skip string
    for i in range(l):
        backstr = reverseme[i] + backstr
        if i % skipchar == 0:
            backstrskip = reverseme[i] + backstrskip

    # store both strings in a tuple and return tuple to function call
    backtuple = (backstr, backstrskip)
    return(backtuple)


def beatstr(whatyear=2017):
    """
    Function is passed a year and defaults to 2017 if missing
    A string is returned based on year being past or future
    """

    # if future year string should include "will"
    if whatyear >= 2017:
        return(" Cubs will beat the ")
    else:
        return(" Cubs beat the ")
