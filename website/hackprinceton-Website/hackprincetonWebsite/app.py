import sys 
import re
import json

SpecialCharacter = {
	'#' : 'if',
	'$' : 'else',
	"*" : "else if",
	"*" : "if else"    
	}

ActionWords = ['Boss', 'going']
string = sys.argv[1]
string = string.lower()
SubStrings = []

string = string.replace("else if", "*")
string = string.replace("if else", "*")
string = string.replace("if", "#")
string = string.replace("else", "$")
string = string + " %"

for index,word in enumerate(string):
	startingIndex = -500
	endingIndex = -500
	if word == "#":
		startingIndex = index
		for i in range(index, len(string)):
			if string[i] == "*":
				endingIndex = i
		SubStrings.append(string[startingIndex:endingIndex])

	elif word == "*":
		startingIndex = index
		for i in range(index, len(string)):
			if string[i] == "$":
				endingIndex = i
		SubStrings.append(string[startingIndex:endingIndex])

	elif word == "$":
		startingIndex = index
		for i in range(index, len(string)):
			if string[i] == "%":
				endingIndex = i
		SubStrings.append(string[startingIndex:endingIndex])


for index,value in enumerate(SubStrings):
	for j in value:
		if j in SpecialCharacter:
			value = value.replace(j, SpecialCharacter[j])
			SubStrings[index] = value
	
print(SubStrings)