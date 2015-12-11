import csv, math, datetime
from dictCreator import creator

R = float(6371000.0)

attributeList = ['apartment_type', 'security_type', 'power_backup_type', 'main_entrance_facing']

f = csv.reader(open('../data/training.csv'))
g = csv.writer(open('../data/working.csv', 'w'))

next(f) # read the header
header = ['x','y','z','price','city_name','locality','per_square_feet_rate','floor_count','floor_number','apartment_type','age_of_property','main_entrance_facing','built_up_area','bedroom_count','bathroom_count','has_swimming_pool','has_gym','number_of_lifts','parking_count','has_gas_pipeline','has_servant_room','power_backup_type','is_gated_community','security_type']

g.writerow(header)

attributeIndex = {}
attributeMap = {}

for attribute in attributeList:
	attributeIndex[attribute] = header.index(attribute)
	attributeMap[attribute] = creator(attribute)

for row in f:
	dateAdded = row[11]

	dateAddedParsed = datetime.date(int(dateAdded[:4]), int(dateAdded[5:7]), int(dateAdded[8:10]))
	todayDate = datetime.datetime.now().date()
	previousYear = todayDate - datetime.timedelta(days=365)
	
	if not previousYear <= dateAddedParsed <= todayDate or not row[9] == 'Apartment':
		continue

	lat = float(row[1])
	lon = float(row[2])
	
	x = R * math.cos(lat) * math.cos(lon)
	y = R * math.cos(lat) * math.sin(lon)
	z = R * math.sin(lat)

	row[0] = x
	row[1] = y
	row[2] = z

	for x in [33, 32, 31, 26, 17, 15, 12, 11, 10, 9]:
		del row[x]
	
	for attribute in attributeList:
		index = attributeIndex[attribute]
		row[index] = attributeMap[attribute][row[index]]

	# special case for number_of_lifts
	indexOfLifts = header.index('number_of_lifts')
	if row[indexOfLifts] == 'None':
		row[indexOfLifts] = 0

	g.writerow(row)