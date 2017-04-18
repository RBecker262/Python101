"""
My Second Awesome Python Module
Author: Robert Becker
Date: April 11, 2017
Purpose: To highlight all Cubs World Series Championsips past and future
Uses: more functions, tuples, for and while loops, exception, if/else

This program creates two files:
One file uses lists and creates a file of past Cubs WS championships
Second file predicts the next 13 Cubs WS championships and whom they beat
"""


# bring needed stringstuff functions into this program for use
from stringstuff import beatstr

# setup lists with past WS championship info
yearlist = [1907, 1908, 2016]
opponentlist = ["Tigers", "Tigers", "Indians"]
serieslist = ["4 - 0", "4 - 1", "4 - 3"]

# open Past Champs output file
champfile = open('../DataFiles/PastChampFile.txt', 'w')

# loop thru list, create record string and write to Past Champs file
for idx in range(len(yearlist)):
    champrec = str(yearlist[idx])
    champrec = champrec + beatstr(yearlist[idx])
    champrec = champrec + opponentlist[idx]
    champrec = champrec + " "
    champrec = champrec + serieslist[idx]
    champrec = champrec + "\n"
    champfile.write(champrec)

# close Past Champs file
champfile.close()

# open future AL Champs file for input and read first record
futureALchampfile = open('../DataFiles/ALChamps.txt', 'r')
futureALchamp = futureALchampfile.readline()

# initialize list to hold future WS champs info, start year at 2017
futurelist = []
year = 2017

# read until eof, for each AL champ create string and append to list
while futureALchamp != "":
    futurechampstr = str(year) + beatstr(year) + futureALchamp
    futurelist.append(futurechampstr)
    futureALchamp = futureALchampfile.readline()
    year = year + 1

# close AL Champ file
futureALchampfile.close()

# open output Future Champs file
Cubsbeatfile = open('../DataFiles/FutChampFile.txt', 'w')

# loop thru list and write each string entry to Future Champs file
for nextwinner in futurelist:
    Cubsbeatfile.write(nextwinner)

# close Future Champs file
Cubsbeatfile.close()
