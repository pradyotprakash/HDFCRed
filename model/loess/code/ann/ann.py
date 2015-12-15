from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
import csv

header = []
trainingData = []
price = []

with open('../../data/working1.csv') as f:
	
	f = csv.reader(f)
	header = next(f)	

	for row in f:
		price.append(row[3])
		del row[3:5]
		trainingData.append(row)

ds = SupervisedDataSet(len(trainingData[0]), 1)

for i in range(len(price)):
	ds.addSample(trainingData[i], price[i])

net = buildNetwork(len(trainingData[0]), 1, 1)
trainer = BackpropTrainer(net, ds)

trainer.trainUntilConvergence(verbose=True, trainingData=ds,)