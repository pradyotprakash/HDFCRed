from sklearn.ensemble import GradientBoostingRegressor
from sklearn import cross_validation
import csv

header = []
X_train = []
y_train = []
X_test = []
y_test = []

data = []
target = []

with open('../../../data/working1.csv') as f:
	
	f = csv.reader(f)
	header = next(f)	

	for row in f:
		target.append(float(row[3]))
		del row[3:5]
		data.append(map(float, row))

X_train, X_test, y_train, y_test = cross_validation.train_test_split(data, target, test_size=0.4, random_state=0)

ensemble = GradientBoostingRegressor()

ensemble.fit(X_train, y_train)

count = 0
for i in range(len(y_test)):
	price = float(y_test[i])
	if -5.0 <= 100*(float(ensemble.predict(X_test[i])) - price)/price <= 5.0:
		count += 1
	print 100*(float(ensemble.predict(X_test[i])) - price)/price

print count, len(y_test)
# print ensemble.predict(['1763.3538916308','5753.496311597','2092.2486098239','0','10000','4','3','0','3','0','450','1','1','0','0','0','1','0','0','0','0','0'])