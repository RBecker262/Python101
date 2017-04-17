"""
My first Python program
Author: Robert Becker
Date: April 11, 2017
Purpose: String manipulation exercise
Uses: user functions, tuples, for and while loops, exception, if/else

Establish 2 strings, concatonate and capitalize first letters, print
Execute function to calculate length of each string
Compare to Python len function for each string, should be the same
Call backwards function to reverse the entire string
Slice the backwards string based on skip count passed to function
Print both backwards strings
"""

# bring needed stringstuff functions into this program for use
from stringstuff import strlen, backwards

# establish strings
name_str = "greetings professor falken!"
game_str = 'shall we play a game?'
hello_str = name_str + ' ' + game_str

# print original strings
print(name_str)
print(game_str)
print(hello_str)

# capitalize and print hello_str
hello_str = name_str.capitalize() + ' ' + game_str.capitalize()
print(hello_str)

# print character count for each string using mine and len functions
print('Length of name string:  ', strlen(name_str), len(name_str))
print('Length of game string:  ', strlen(game_str), len(game_str))
print('Length of hello string: ', strlen(hello_str), len(hello_str))

# call function to reverse entire and a second with every nth byte
rev_tuple = backwards(hello_str, 3)
for revtup in rev_tuple:
    print(revtup)
