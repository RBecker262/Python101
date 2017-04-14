# My first Python program
# Author: Robert Becker
# Date: April 11, 2017
# Purpose: String manipulation using user defined functions, tuples, for and while loops, exception, if/elif

# Establish 2 strings then concatonate and capitalize first letters and print
# Execute my function to calculate length of each string and compare to len function for each string, should be the same
# Call another function to reverse the entire string and slice the backwards string based on skip count passed to function

def mainline():

	# establish strings
	name_str = "greetings professor falken!"
	game_str = 'would you like to play a game?'
	hello_str = name_str + ' ' + game_str

	# print original strings
	print(name_str)
	print(game_str)
	print(hello_str)

	# capitalize and print hello_str
	hello_str = name_str.capitalize() + ' ' + game_str.capitalize()
	print(hello_str)

	# print character count for each string using mine and len functions
	print('Length of name string:  ',strlen(name_str),len(name_str))
	print('Length of game string:  ',strlen(game_str),len(game_str))
	print('Length of hello string: ',strlen(hello_str),len(hello_str))

	# call function to reverse hello_string with all bytes and a second with every nth byte
	rev_tuple = backwards(hello_str,3.2)
	for rt in rev_tuple:
		print(rt)

def strlen(countstr):

	# string index starts at 0, not 1. loop until IndexError (end of string)
	i = 0

	while True:

		try:
	 		string1 = countstr[i]
	 		i = i + 1				# this could be done under else: instead
		except IndexError as whyme:	# whyme contains the error that occurred
	 		return (i)

def backwards(reverseme,skipchar):

	# creates a string with characters reversed and a sliced version of same based on passed parameter
	backstr = ""
	backstrskip = ""
	l = strlen(reverseme)

	if skipchar < 0 or skipchar > l:
		skipchar = 1
	elif skipchar != int(skipchar):
		skipchar = int(skipchar)

	# slice thru string and create reverse string plus skip string
	for i in range(l):
		backstr = reverseme[i] + backstr
		if i % skipchar == 0:
			backstrskip = reverseme[i] + backstrskip

	# store both backward strings in a tuple and return the tuple to the assignment statement
	newtuple = (backstr, backstrskip)
	return(newtuple)

mainline()
