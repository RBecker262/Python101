# My first Python program
# Author: Robert Becker
# Date: April 11, 2017
# Purpose: Random displays and string manipulation

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

	# call function to reverse hello_string with every other byte
	rev_string = backwards(hello_str,3.2)
	print(rev_string)

def strlen(countstr):

	# string index starts at 0, not 1
	i = 0

	while True:

		try:
	 		string1 = countstr[i]
		except IndexError as whyme:
	 		# print('String error due to:',whyme)
	 		return (i)
		else:
			i = i + 1

def backwards(reverseme,skipchar):

	# creates a string with characters reversed and
	newme = ""
	newmeskip = ""
	l = strlen(reverseme)
	if skipchar < 0 or skipchar > l:
		skipchar = 1
	elif skipchar != int(skipchar):
		skipchar = int(skipchar)

	# loop thru string and create reverse string plus skip string
	for i in range(l):
		newme = reverseme[i] + newme
		if i % skipchar == 0:
			newmeskip = reverseme[i] + newmeskip

	# print the entire string backwards then return desired result
	print(newme)
	return(newmeskip)

mainline()