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
		price.append(float(row[3]))
		del row[3:5]
		trainingData.append(map(float, row))

ds = SupervisedDataSet(len(trainingData[0]), 1)

for i in range(len(price)):
	ds.addSample(trainingData[i], price[i])

net = buildNetwork(len(trainingData[0]), 20, 1)
trainer = BackpropTrainer(net, ds)

trainer.train()
print net.activate((1763.3538916308,5753.496311597,2092.2486098239,0,4,3,0,3,0,450,1,1,0,0,0,1,0,0,0,0,0))