import csv, pprint, math
import numpy as np
from numpy.linalg import inv

np.set_printoptions(threshold=np.nan)
error_file = open('error_log_latLong', 'w')

r = 1.0
delta = 1.0

trainingData = []
header = []

def weightF(p, q):
	p = map(float, p)
	q = map(float, q)

	x = 0.0
	for i in range(len(p)):
		x += ((p[i]) - (q[i]))**2

	x = math.sqrt(x)
	x = x/r
	
	if x >= 1 or x <= 0.0:
		return 0.0
	else:
		return x

indexOfLocality = ''
indexOfPrice = ''

with open('../data/working.csv') as f:

	f = csv.reader(f)
	header = next(f)	

	indexOfLocality = header.index('locality')
	indexOfPrice = header.index('price')

	for row in f:
		trainingData.append(row)

def fitModel(testData = ['1778.8039396552','5756.1558987142','2071.7545255086','16800000','Mumbai','Agripada','26880','7','4','0','12','7','625','1','1','0','0','1','0','0','0','0','1','2']):
	
	Y = []
	W = []
	X = []

	for row in trainingData:
		ret = weightF(row[:3], testData[:3])

		if not ret <= 0.0: # is within the radius and consider it
			Y.append([float(row[indexOfPrice])])
			W.append((1 - ret**2)**2)
			X.append(map(float, row[6:]))

	Y = np.matrix(Y)
	X = np.matrix(X)
	W = np.diag(W)
	I = np.eye(X.shape[1])
	X_transpose = X.transpose()

	beta = inv(X_transpose * W * X + delta*I) * X_transpose * W * Y
	phi_x = np.matrix(map(float, testData[6:]))

	return float(phi_x * beta)

def testModel():

	with open('../data/working.csv', 'r') as f:
		f = csv.reader(f)
		next(f) # skip the header

		for row in f:
			price = float(row[indexOfPrice])
			try:
				val = 100*(fitModel(row) - price)/price
				print val
			except Exception as e:
				error_file.write('Error in date item: ' + str(row) + '\n')

testModel()