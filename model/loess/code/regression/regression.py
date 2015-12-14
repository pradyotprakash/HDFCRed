import csv, pprint, math
import numpy as np
from numpy.linalg import inv, det, solve

np.set_printoptions(threshold=np.nan)
error_file = open('error_log_regression', 'w')

r = 1.0
delta = 1.0

trainingData = {}
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
		return (1 - x**2)**2

indexOfLocality = ''
indexOfPrice = ''

with open('../data/working.csv') as f:
	
	f = csv.reader(f)
	header = next(f)	

	indexOfLocality = header.index('locality')
	indexOfPrice = header.index('price')

	for row in f:
		locality = row[indexOfLocality]

		if locality in trainingData:
			trainingData[locality].append(row)
		else:
			trainingData[locality] = [row]

def fitModel(testData = ['1778.8039396552','5756.1558987142','2071.7545255086','16800000','Mumbai','Agripada','26880','7','4','0','12','7','625','1','1','0','0','1','0','0','0','0','1','2']):
	localData = trainingData[testData[indexOfLocality]]

	Y = []
	W = []
	X = []

	for row in localData:
		Y.append([float(row[indexOfPrice])])
		W.append(weightF(row[0:3], testData[0:3]))
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
	count = 0
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