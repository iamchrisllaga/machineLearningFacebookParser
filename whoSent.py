from random import randint
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split

import convertToTrainingData

def loadData() :
	data, labels, packetSize = convertToTrainingData.main()
	data = np.array(data)
	labels = np.array(labels)
	data = data/10000.0
	trainingData, testingData, trainingLabels, testingLabels = train_test_split(data, labels, test_size=0.25, random_state=randint(0, 100))
	lb = LabelBinarizer()
	trainingLabels = lb.fit_transform(trainingLabels)
	testingLabels = lb.transform(testingLabels)
	numClasses = len(lb.classes_)
	print(trainingData[:3])
	print(trainingLabels[:3])
	print(testingData[:3])
	print(testingLabels[:3])
	return trainingData, trainingLabels, testingData, testingLabels, packetSize, numClasses

def createModel(packetSize, numClasses) :
	model = keras.Sequential([
		keras.layers.Flatten(),
		keras.layers.Dense(128, activation='relu'),
		keras.layers.Dense(numClasses, activation='softmax')
		])
	model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
	return model

def trainModel(model, trainingData, trainingLabels, cycles) :
	indexedTrainingLabels = np.argmax(trainingLabels, axis=1)
	model.fit(trainingData, indexedTrainingLabels, epochs=cycles)
	return model

def testModel(model, testingData, testingLabels) :
	prediction = model.predict(testingData)
	for x in range(10) :
		actual = np.argmax(testingLabels[x], axis=0)
		predict = np.argmax(prediction[x])
		print('Actual: %s\nPrediction: %s' % (actual, predict))

def main() :
	cycles = 5
	trainingData, trainingLabels, testingData, testingLabels, packetSize, numClasses = loadData()
	model = createModel(packetSize, numClasses)
	model = trainModel(model, trainingData, trainingLabels, cycles)
	testModel(model, testingData, testingLabels)
	print('done')

if __name__ == '__main__':
    main()