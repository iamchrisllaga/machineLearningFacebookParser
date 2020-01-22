import getData
import pprint
import os

def standardizePackets(messages, dataSize, dictionary) :
	data = []
	labels = []
	#nameDict = {}
	#counter = 0
	for message in messages :
		#if(message[0] not in nameDict) :
		#	nameDict[message[0]] = counter
		#	counter += 1
		try :
			content = message[1].split(' ')
			content = encode(content, dictionary)
			if(len(content) < dataSize) :
				content = content + ([0] * (dataSize - len(content)))
			elif(len(content) > dataSize) :
				content = content[:dataSize]
		except :
			content = [0] * dataSize
		timestamp = [message[2]]
		#data.append(content + timestamp)
		data.append(content)
		#labels.append(nameDict[message[0]])
		labels.append(message[0])
	#return data, labels, nameDict
	return data, labels

def convertFreqTable(frequency, top) :
	dictionaryList = []
	counter = 1
	for wordPair in frequency :
		dictionaryList.append([wordPair[1], counter])
		counter += 1
	dictionary = {pair[0]:pair[1] for pair in dictionaryList}
	return dictionary

def splitTrainTest(data, labels, percentageForTraining) :
	if(len(data) == len(labels)) :
		size = len(data)
	else :
		sys.exit('Data length and labels length not the same.')
	trainingSize = int(size * percentageForTraining)
	trainingData = data[:trainingSize]
	trainingLabels = labels[:trainingSize]
	testingData = data[trainingSize:]
	testingLabels = labels[trainingSize:]
	return trainingData, trainingLabels, testingData, testingLabels

def flatten(array) :
	flattened = []
	for cell in array :
		for data in cell :
			flattened.append(data)
	return flattened

def encode(message, dictionary) :
	encoded = []
	for word in message :
		encoded.append(dictionary.get(word, 0))
	return encoded

def printToFile(list, file) :
	logFile = file
	with open(logFile, 'wt') as out :
		pprint.pprint(list, stream=out)

def main() :
	messageSize = 32
	mostFrequentWords = 9999
	fullLog, wordFreq = getData.main()
	#data, labels, nameDict = standardizePackets(fullLog, messageSize)
	dictionary = convertFreqTable(wordFreq, mostFrequentWords)
	data, labels = standardizePackets(fullLog, messageSize, dictionary)
	#trainingData, trainingLabels, testingData, testingLabels = splitTrainTest(data, labels, .9)
	printToFile(data, 'data.txt')
	printToFile(labels, 'labels.txt')
	return data, labels, (messageSize)

if __name__ == '__main__':
    main()
