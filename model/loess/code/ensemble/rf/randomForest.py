# from sklearn.ensemble import RandomForestRegressor
# from sklearn import cross_validation
# import csv

# header = []
# X_train = []
# y_train = []
# X_test = []
# y_test = []

# data = []
# target = []

# with open('../../../data/working1.csv') as f:
	
# 	f = csv.reader(f)
# 	header = next(f)	

# 	for row in f:
# 		target.append(float(row[3]))
# 		del row[3:5]
# 		data.append(map(float, row))

# X_train, X_test, y_train, y_test = cross_validation.train_test_split(data, target, test_size=0.1, random_state=0)

# ensemble = RandomForestRegressor()

# ensemble.fit(X_train, y_train)

# count = 0
# for i in range(len(y_test)):
# 	price = float(y_test[i])
# 	if -5.0 <= 100*(float(ensemble.predict(X_test[i])) - price)/price <= 5.0:
# 		count += 1
# 	print 100*(float(ensemble.predict(X_test[i])) - price)/price

# print count, len(y_test)
# # print ensemble.predict(['1763.3538916308','5753.496311597','2092.2486098239','0','4','3','0','3','0','450','1','1','0','0','0','1','0','0','0','0','0'])





from sklearn.ensemble import RandomForestRegressor
from sklearn import cross_validation
import csv

dataDict = {}
header = []
error_file = open('error.log', 'w')

with open('../../../data/working1.csv') as f:
	
	f = csv.reader(f)
	header = next(f)	

	for row in f:
		locality = row[5]
		t = (map(float, row[:3] + row[5:]), float(row[3]))
		if locality in dataDict:
			dataDict[locality].append(t)
		else:
			dataDict[locality] = [t]

with open('../../../data/working1.csv') as f:
	
	f = csv.reader(f)
	next(f)

	for row in f:
		try:
			locality = row[5]
			training = dataDict[locality]
			
			data = []
			target = []
			t = (map(float, row[:3] + row[5:]), float(row[3]))

			for x in training:
				if not x == t:
					data.append(x[0])
					target.append(x[1])

			# X_train, X_test, y_train, y_test = cross_validation.train_test_split(data, target, test_size=0.1, random_state=0)

			ensemble = RandomForestRegressor()
			ensemble.fit(data, target)

			print 100.0*(ensemble.predict(t[0]) - t[1])/t[1]
		except Exception as e:
			error_file.write('Exception: ' + str(e) + '\n' + str(row) + '\n\n')