import pandas as pd
import math
import os
import enchant
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from DigiPsych_API.lang_check import language_check

engDict = enchant.Dict("en_US")

def removePeriods(wordList):
	for each in range(len(wordList)):
		if '.' in wordList[each]:
			wordList[each] = wordList[each].replace(".", "")
	return wordList

def unintellWordRatio(transcript):
	transcript = removePeriods(transcript)
	unintell = 0
	for each in transcript:
		if each == '': continue
		if not engDict.check(each): unintell += 1
		if each == '<unintelligible>': unintell += 1
	return float(unintell)/float(len(transcript))

def numberRatio(transcript):
	transcript = removePeriods(transcript)
	numbers = 0
	numbs = '1234567890'
	for each in transcript:
		for letter in each:
			if letter in numbs:
				numbers += 1
				break
	return float(numbers)/float(len(transcript))

def brunetIndex(transcript):
	vocab = 0
	wordsUsed = {}
	for each in transcript:
		if each not in wordsUsed:
			wordsUsed[each] = 1
			vocab += 1
		else:
			wordsUsed[each] += 1
	return len(transcript)**(vocab**(-.165))

def honoreStat(transcript):
	transcript = removePeriods(transcript)
	V1 = []
	V = []
	for each in transcript:
		V1.append(each) if each not in V1 else V1.pop(V1.index(each))
		if each not in V: V.append(each) 
	try:
		return 100 * math.log(float(len(transcript))/(1 - (float(len(V1))/float(len(V)))))
	except:
		return 0

def suffixRatio(transcript):
	transcript = removePeriods(transcript)
	ps = PorterStemmer()
	suffixNumber = 0
	word = {}
	count = 0
	try:
		for each in transcript:
			if ps.stem(each) != each:
				suffixNumber += 1
			if each not in word:
				word[each] = 1
				count += 1
	except:
		pass
	return float(suffixNumber)/float(count)

def typetokenratio(transcript):
	transcript = removePeriods(transcript)
	ps = PorterStemmer()
	unique = 0
	wordsUsed = {}
	for each in transcript:
		if each not in wordsUsed:
			wordsUsed[each] = 1
			unique += 1
	return float(unique)/float(len(transcript))

def lingComplexResult(path):
	with open(path, encoding = "utf-8", errors='ignore') as word_list:
		rawText = word_list.read()
		inputTranscript = rawText.split(' ')
	output = [path, unintellWordRatio(inputTranscript), 
	numberRatio(inputTranscript), 
	brunetIndex(inputTranscript), 
	honoreStat(inputTranscript), 
	suffixRatio(inputTranscript), 
	typetokenratio(inputTranscript)]
	return output

def ling_complex(path, path2):
	overall = []
	fi = path
	overall.append(lingComplexResult(fi))
	overall.append(lingComplexResult(path2))
	lingComplex_df = pd.DataFrame(data = overall, columns = ['Unintelligble', 'Number Ratio', 'Brunet Index', 'Honore Stat', 'Suffix Ratio', 'Type Token Ratio'], index = [fi, path2])
	file_name = '/Users/abbad/Desktop/Research/LinguisticFeatures/' + 'test' + '.csv'
	lingComplex_df.to_csv(file_name)
	return lingComplex_d