import csv, pprint, math
import numpy as np
from numpy.linalg import inv

r = 1000.0

trainingData = {}
header = []
testData = ['-4606720.347024485','-3911087.669195922','2017712.0429273888','4500000','Mumbai','Mulund East','10000','4','3','0','3','0','450','1','1','0','0','0','1','0','0','0','0','0']

def weightF(p, q):
	p = map(float, p)
	q = map(float, q)

	x = 0.0
	for i in range(len(p)):
		x += (p[i] - q[i])**2

	x = math.sqrt(x)/r
	
	if x > 1:
		return 0.0
	else:
		return (1 - x**2)**2

with open('../data/working.csv') as f:
	
	f = csv.reader(f)
	header = next(f)	

	indexOfLocality = header.index('locality')

	for row in f:
		locality = row[indexOfLocality]

		if locality in trainingData:
			trainingData[locality].append(row)
		else:
			trainingData[locality] = [row]

localData = trainingData[testData[indexOfLocality]]

# local regression begins here

indexOfPrice = header.index('price')
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

X_transpose = X.transpose()

beta = inv(X_transpose * W * X) * X_transpose * W * Y
print beta