import csv, os
import numpy as np

np.set_printoptions(precision=4)

trainingData = {}
header = []

with open('../../data/working.csv') as f:

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

for local in trainingData:
	path = 'points/' + ''.join(local.split(' ')) + '/'
	os.system('mkdir ' + path)
	f = trainingData[local]
	X = []
	for row in f:
		X.append(map(float, row[6:]))
	X = np.matrix(X).transpose()
	
	l = len(X)
	for i in range(l):
		a = X[i].tolist()[0]
		for j in range(l):
			if not i == j:
				b = X[j].tolist()[0]
				g = open('tmp.gp', 'w')
				for k in range(len(a)):
					g.write(str(a[k]) + ' ' + str(b[k]) + '\n')
				g.close()
				command = 'gnuplot -e "filename=\'' + path + str(i) + '_' + str(j) + '.svg\'" plot.p'
				# print command
				os.system(command)
				os.system('rm tmp.gp')