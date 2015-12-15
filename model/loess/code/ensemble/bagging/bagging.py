from sklearn.ensemble import BaggingRegressor
import csv

header = []
X_train = []
y_train = []

with open('../../../data/working1.csv') as f:
	
	f = csv.reader(f)
	header = next(f)	

	for row in f:
		y_train.append(row[3])
		del row[3:5]
		X_train.append(row)

ensemble = BaggingRegressor()

ensemble.fit(X_train, y_train)
print ensemble.predict(['1763.3538916308','5753.496311597','2092.2486098239','0','10000','4','3','0','3','0','450','1','1','0','0','0','1','0','0','0','0','0'])