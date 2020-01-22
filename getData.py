import json
import glob, os
import pprint

def readConversation(jsonFile) :
	with open(jsonFile, 'r', encoding='latin1') as jsonFile:
		data = json.load(jsonFile)
		messages = data['messages']
		messages.reverse()
		messageArray = []
		for cell in messages :
			packet = []
			packet.append(cell['sender_name'])
			try :
				packet.append(cell['content'])
			except :
				packet.append(None)
			packet.append(cell['timestamp_ms'])
			messageArray.append(packet)
	return messageArray

def wordCount(messageArray) :
	dictionary = {}
	for message in messageArray :
		text = message[1]
		try :
			text = text.split(' ')
			for word in text :
				dictionary[word] = dictionary.get(word, 0) + 1
		except :
			pass
	wordFreq = []
	for key, value in dictionary.items() :
		wordFreq.append((value, key))
	wordFreq.sort(reverse = True)
	return wordFreq

def findAllJSON(path) :
	completeArray = []
	for file in glob.glob(path) :
		messageArray = readConversation(file)
		completeArray = completeArray + messageArray
	return completeArray

def printToFile(list, file) :
	logFile = file
	with open(logFile, 'wt') as out :
		pprint.pprint(list, stream=out)

def main() :
	fullLog = findAllJSON('data/*.json')
	wordFreq = wordCount(fullLog)
	printToFile(wordFreq, 'wordFreq.txt')
	printToFile(fullLog, 'fullLog.txt')
	return fullLog, wordFreq


if __name__ == '__main__':
    main()