# Robert Second Program
# Date: April 12, 2017
# Work with lists to create a file of Cubs World Championships past and future
# Added newline character to end of each record
# Created function with established default value for passed paraameter

def mainline():

	yearlist = [1907, 1908, 2016, 2017]
	opponentlist = ["Tigers", "Tigers", "Indians", "Red Sox"]
	serieslist = ["4 - 0", "4 - 1", "4 - 3", "4 - 3"]

	champfile = open('ChampFile.txt', 'w')

	for i in range(len(yearlist)):
		if yearlist[i] == 2017:
			beatit = beatstr()
		else:
			beatit = beatstr(yearlist[i])
		champrec = str(yearlist[i]) + beatit + opponentlist[i] + " " + serieslist[i] + "\n"
		champfile.write(champrec)

	champfile.close()

def beatstr(whatyear = 2017):
	if whatyear == 2017:
		return(" Cubs will beat the ")
	else:
		return(" Cubs beat the ")

mainline()
