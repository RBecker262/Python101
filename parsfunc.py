


def dictlevel(indict, inlevel):

    keylist = list(indict.keys())

    for dictkey in keylist:
        outputstr = 'Level ' + str(inlevel) + ' ' + dictkey + ' '
        if type(indict[dictkey]) is dict:
            print(outputstr + 'Subdictionary')
            dictlevel(indict[dictkey], inlevel+1)
        else:
            print(outputstr + str(indict[dictkey]))
