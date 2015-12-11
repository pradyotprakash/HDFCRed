import csv, pprint, math

R = float(6371000.0)

class Data:
	def __init__(self, l):
		self.data = l

trainingData = {}
header = []
testData = []

def weightF(x):
	x = math.abs(x)
	if x > 1:
		return 0.0
	else:
		return (1 - x**2)**2


with open('../data/working.csv') as f:
	header = f.readline() # take care the the newline character
	header += ',x_coor,y_coor,z_coor'

	f = csv.reader(f)
		
	for row in f:
		locality = row[3]
		lat = float(row[0])
		lon = float(row[1])
		
		x = R * math.cos(lat) * math.cos(lon)
		y = R * math.cos(lat) * math.sin(lon)
		z = R * math.sin(lat)

		row.append(x)
		row.append(y)
		row.append(z)

		todayDate = datetime.datetime.now().date()
		oneYearBack = todayDate - datetime.timedelta(days=365)
		dateAdded = row[8]
		
		dateAdded = datetime.date(int(dateAdded[:4]), int(dateAdded[5:7], int(dateAdded[8:10])))
		row[8] = dateAdded

		del row[1] # remove latitude
		del row[0] # remove longitude

		if oneYearBack < dateAdded < todayDate:
			if locality in trainingData:
				trainingData[locality].append(row)
			else:
				trainingData[locality] = [row]



# begin application of local regression below

from scipy.linalg import expm
import numpy as np
a = np.array()

