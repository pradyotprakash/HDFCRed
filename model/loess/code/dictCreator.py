import csv

def creator(currentAttribute = 'apartment_type'):
	current = 0

	f = csv.reader(open('../data/training.csv'))
	d = {}

	header = next(f)
	index = header.index(currentAttribute)
	
	for row in f:
		value = row[index].strip()

		if value not in d:
			d[value] = str(current)
			current += 1

	return d	