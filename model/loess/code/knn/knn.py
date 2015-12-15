import csv, math
import numpy as np

np.set_printoptions(threshold=np.nan)
error_file = open('error_log_knn', 'w')

k = 10
r = 2.0

trainingData = []
header = []

def geometricDistance(p, q):
	x = 0.0
	for i in range(len(p)):
		x += ((p[i]) - (q[i]))**2

	if math.sqrt(x) <= r:
		return True
	else: return False	

indexOfPrice = ''

with open('../../data/working.csv') as f:

	f = csv.reader(f)
	header = next(f)	
	header = header[:4] + header[6:]

	indexOfPrice = header.index('price')

	for row in f:
		trainingData.append(map(float, row[:3] + [float(row[3])/10000000.0] + row[6:]))

def fitModel(testData = ['1778.8039396552','5756.1558987142','2071.7545255086','16800000','26880','7','4','0','12','7','625','1','1','0','0','1','0','0','0','0','1','2']):
	
	withDistance = []	
	for row in trainingData:
		if not testData == row:
			dist = distance(row, testData)
			withDistance.append(row + [dist])

	withDistance.sort(key=lambda x:x[-1])
	
	price = 0.0	
	for i in range(k):
		price += withDistance[i][indexOfPrice]

	return price/k

def testModel():
	for row in trainingData:
		price = row[indexOfPrice]
		try:
			x = fitModel(row)
			val = 100*(x - price)/price
			print val
		except Exception as e:
			error_file.write('Error in test item: ' + str(row) + '\n')

testModel()