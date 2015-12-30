import csv, math, datetime
from dictCreator import creator

R = float(6371.0)

attributeList = ['apartment_type', 'security_type', 'power_backup_type', 'main_entrance_facing']
toBeDeleted = ['city_name', 'per_square_feet_rate', 'locality', 'neighbourhood_score', 'region_name', 'is_society_formed', 'water_supply_type', 'status', 'age_of_property_date', 'available_from', 'date_added', 'under_construction', 'property_type']

f = csv.reader(open('../../data/training.csv', 'r'))
g = csv.writer(open('./working22.csv', 'w'))

originalHeader = next(f) # read the header
header = ['x','y','z','price','floor_count','floor_number','apartment_type','age_of_property','main_entrance_facing','built_up_area','bedroom_count','bathroom_count','has_swimming_pool','has_gym','number_of_lifts','parking_count','has_gas_pipeline','has_servant_room','power_backup_type','is_gated_community','security_type']

indexOfToBeDeleted = []
for attr in toBeDeleted:
	indexOfToBeDeleted.append(originalHeader.index(attr))

indexOfToBeDeleted.sort(reverse=True)

g.writerow(header)

attributeIndex = {}
attributeMap = {}

for attribute in attributeList:
	attributeIndex[attribute] = header.index(attribute)
	attributeMap[attribute] = creator(attribute)

open('./attributeMap', 'w').write(str(attributeMap))

for row in f:
	dateAdded = row[originalHeader.index('date_added')]

	dateAddedParsed = datetime.date(int(dateAdded[:4]), int(dateAdded[5:7]), int(dateAdded[8:10]))
	todayDate = datetime.datetime.now().date()
	previousYear = todayDate - datetime.timedelta(days=365)
	
	if not previousYear <= dateAddedParsed <= todayDate or not row[9] == 'Apartment':
		continue

	lat = float(row[1])*(math.pi/180.0)
	lon = float(row[2])*(math.pi/180.0)
	
	x = R * math.cos(lat) * math.cos(lon)
	y = R * math.cos(lat) * math.sin(lon)
	z = R * math.sin(lat)

	row[0] = x
	row[1] = y
	row[2] = z

	for i_ in indexOfToBeDeleted:
		del row[i_]
	
	for attribute in attributeList:
		index = attributeIndex[attribute]
		row[index] = attributeMap[attribute][row[index]]

	# special case for number_of_lifts
	indexOfLifts = header.index('number_of_lifts')
	if row[indexOfLifts] == 'None':
		row[indexOfLifts] = 0

	g.writerow(row)