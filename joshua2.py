# My second Python program (functions only, execution of mainline is in cubswin.py)
# Author: Robert Becker
# Date: April 12, 2017
# Purpose: Work with lists, file i/o, for and while loops, if/else

# Work with lists to create a file of Cubs World Championships past and future
# First create file of past championships by using for to loop thru lists and creating strings to output file
# Next create file of future WS victories by using while to read AL champs file, appending strings to a list, then using for loop to write list entries to a file
# Created function with established default value for passed paraameter

def mainline():

	# Setup lists and then loop thru lists to create past WS champions file
	# Created function to determine if "Cubs beat" or "Cubs will beat" string in each output record
	yearlist = [1907, 1908, 2016]
	opponentlist = ["Tigers", "Tigers", "Indians"]
	serieslist = ["4 - 0", "4 - 1", "4 - 3"]

	champfile = open('../DataFiles/PastChampFile.txt', 'w')

	for i in range(len(yearlist)):
		champrec = str(yearlist[i]) + beatstr(yearlist[i]) + opponentlist[i] + " " + serieslist[i] + "\n"
		champfile.write(champrec)

	champfile.close()

	# Create future champ file using ALChamps as input and store strings to a list using append
	futureALchampfile = open('../DataFiles/ALChamps.txt', 'r')
	futureALchamp = futureALchampfile.readline()

	# Initialize list and counter variable
	futurelist = []
	i = 0

	# Loop until null values (eof), create champ string and append to list, then add to count and read next record
	while futureALchamp != "":
		year = i + 2017
		futurechampstr = str(year) + beatstr(year) + futureALchamp
		futurelist.append(futurechampstr)
		i = i + 1
		futureALchamp = futureALchampfile.readline()

	futureALchampfile.close()

	# Open output Future Champs file, loop through future champs list and write each entry to file
	# I did not need to add the \n at the end of the record because the AL Champs input already had the newline character at the end of each input string
	Cubsbeatfile = open('../DataFiles/FutureChampFile.txt', 'w')

	for y in futurelist:
		Cubsbeatfile.write(y)

	Cubsbeatfile.close()

def beatstr(whatyear = 2017):

	# Set default to 2017 if not provided. If future year string should include "will"
	if whatyear >= 2017:
		return(" Cubs will beat the ")
	else:
		return(" Cubs beat the ")
